"""

Query Methods to retieve and update database data

Notes: 

- Change get_cat to go through market hashname and filter through the predefined weapons object

"""

import psycopg
import config as cfg
import scripts.skin_port as sp

# Database Class that holds all query methods
class Database:
    def __init__(self,database_url: str):
        self.database_url = database_url
        self.table_names: list[str] = []

    # determines what category the incoming item is
    # We can use the market page attribute to get the item category
    # Ex) 'https://skinport.com/market/smg/ump-45?item=Primal%20Saber' - here we can extract the 'smg' part. 
    def get_cat(self,url):
        lowered_cat = [item.lower() for item in cfg.CATEGORIES]
        result = url.split("/")
        for item in lowered_cat:
            if item in url.lower():
                result = result[4]
                print(result)
                return result

        # Ex) the category format is like 'https://skinport.com/market/collectible?item=Office+Pin' 
        result = result[4].split("?")
        #print(result[0])
        return result[0]

    # Creating a simple database connection
    def connect_to_database(self):
        try:
            return psycopg.connect(self.database_url)
        except Exception as error:
            print(error)

    def get_source_id(self,cur,source_name: str = "Skinport"):
        query = """
            SELECT source_id
            FROM sources
            WHERE name = %s;
        """

        cur.execute(query,(source_name,))
        result = cur.fetchone()

        if result is None:
            raise ValueError(
                f"Source '{source_name}' does not exist."
            )

        return result[0]

    def make_run(self,cur,source_id: int,currency: str,items_received: int):
        query = """
            INSERT INTO runs (
                source_id,
                currency,
                items_received
            )
            VALUES (%s, %s, %s)
            RETURNING run_id;
        """

        cur.execute(
            query,
            (
                source_id,
                currency,
                items_received
            )
        )

        return cur.fetchone()[0]

    # insert/update database information with a new run
    # if there is nothing to add, only new prices of items are added. 
    def insert(self):
        conn = None
        cur = None
        run_counter = 0

        try:
            conn = self.connect_to_database()
            cur = conn.cursor()
            data = sp.get_sp_json()

            query_source = """
                INSERT INTO sources (name)
                VALUES (%s)
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                RETURNING source_id;
            """
            cur.execute(query_source, ("Skinport",))
            source_id = cur.fetchone()[0]

            run_id = self.make_run(cur, source_id, "CAD", len(data))

            # process each item that we got from the API
            # Note: these tables shouldn't have duplicate values, if we are updating in our run, just update the prices table
            # if there is nothing new to add. 
            # AlSO, I only want to insert items that are in the constant category object
            for item in data:
                category = self.get_cat(item["market_page"])
                if category.lower() not in [item.lower() for item in cfg.CATEGORIES]:
                    continue

                match = cfg.SKIN_PATTERN.match(item["market_hash_name"])
                if match is None:
                    continue

                category_query = """
                    SELECT category_id
                    FROM item_categories
                    WHERE LOWER(name) = LOWER(%s);
                """
                cur.execute(category_query, (category,))
                category_id = cur.fetchone()[0]

                query_items = """
                    INSERT INTO items (
                        market_hash_name,
                        display_name,
                        category_id,
                        is_stattrak,
                        is_souvenir
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (market_hash_name) DO UPDATE SET
                        display_name = EXCLUDED.display_name,
                        category_id = EXCLUDED.category_id,
                        is_stattrak = EXCLUDED.is_stattrak,
                        is_souvenir = EXCLUDED.is_souvenir,
                        last_seen_at = NOW(),
                        active = TRUE
                    RETURNING item_id;
                """
                market_hash_name = item["market_hash_name"]
                cur.execute(
                    query_items,
                    (
                        market_hash_name,
                        market_hash_name,
                        category_id,
                        market_hash_name.startswith("StatTrak™ "),
                        market_hash_name.startswith("Souvenir "),
                    ),
                )
                item_id = cur.fetchone()[0]

                weapon_query = """
                    SELECT weapon_id
                    FROM weapons
                    WHERE name = %s;
                """
                cur.execute(weapon_query, (match["weapon"],))
                weapon = cur.fetchone()
                weapon_id = weapon[0] if weapon is not None else None

                exterior_query = """
                    SELECT exterior_id
                    FROM exteriors
                    WHERE name = %s;
                """
                cur.execute(exterior_query, (match["exterior"],))
                exterior = cur.fetchone()
                exterior_id = exterior[0] if exterior is not None else None

                query_details = """
                    INSERT INTO skin_details (
                        item_id,
                        weapon_id,
                        skin_name,
                        exterior_id
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (item_id) DO UPDATE SET
                        weapon_id = EXCLUDED.weapon_id,
                        skin_name = EXCLUDED.skin_name,
                        exterior_id = EXCLUDED.exterior_id;
                """
                cur.execute(
                    query_details,
                    (item_id, weapon_id, match["skin"], exterior_id),
                )

                query_prices = """
                    INSERT INTO item_prices (
                        item_id,
                        run_id,
                        min_price,
                        max_price,
                        mean_price,
                        median_price,
                        suggested_price,
                        quantity
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (item_id, run_id) DO UPDATE SET
                        min_price = EXCLUDED.min_price,
                        max_price = EXCLUDED.max_price,
                        mean_price = EXCLUDED.mean_price,
                        median_price = EXCLUDED.median_price,
                        suggested_price = EXCLUDED.suggested_price,
                        quantity = EXCLUDED.quantity;
                """
                cur.execute(
                    query_prices,
                    (
                        item_id,
                        run_id,
                        item.get("min_price"),
                        item.get("max_price"),
                        item.get("mean_price"),
                        item.get("median_price"),
                        item.get("suggested_price"),
                        item.get("quantity"),
                    ),
                )

                run_counter += 1

            query_complete_run = """
                UPDATE runs
                SET completed_at = NOW(),
                    status = 'success',
                    items_inserted = %s
                WHERE run_id = %s;
            """
            cur.execute(query_complete_run, (run_counter, run_id))

            conn.commit()
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

# a simple function that tests our database connectivity
def test_conn():
    testdb = Database(cfg.DATABASE_URL)
    print(testdb.connect_to_database())

def run_bot():
    testdb = Database(cfg.DATABASE_URL)
    testdb.insert()