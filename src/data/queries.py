"""

Query Methods to retieve and update database data

Notes: 


"""

import psycopg
import re
import config as cfg
import scripts.skin_port as sp


# Constant Data

EXTERIOR_ORDER = {
    "Factory New": 1,
    "Minimal Wear": 2,
    "Field-Tested": 3,
    "Well-Worn": 4,
    "Battle-Scarred": 5,
}

WEAPON_TYPES = {

    "CZ75-Auto": "Pistol",
    "Desert Eagle": "Pistol",
    "Dual Berettas": "Pistol",
    "Five-SeveN": "Pistol",
    "Glock-18": "Pistol",
    "P2000": "Pistol",
    "P250": "Pistol",
    "R8 Revolver": "Pistol",
    "Tec-9": "Pistol",
    "USP-S": "Pistol",

    "AK-47": "Rifle",
    "AUG": "Rifle",
    "AWP": "Rifle",
    "FAMAS": "Rifle",
    "G3SG1": "Rifle",
    "Galil AR": "Rifle",
    "M4A1-S": "Rifle",
    "M4A4": "Rifle",
    "SCAR-20": "Rifle",
    "SG 553": "Rifle",
    "SSG 08": "Rifle",

    "MAC-10": "SMG",
    "MP5-SD": "SMG",
    "MP7": "SMG",
    "MP9": "SMG",
    "P90": "SMG",
    "PP-Bizon": "SMG",
    "UMP-45": "SMG",

    "MAG-7": "Heavy",
    "Nova": "Heavy",
    "Sawed-Off": "Heavy",
    "XM1014": "Heavy",
    "M249": "Heavy",
    "Negev": "Heavy",

    "Bayonet": "Knife",
    "Bowie Knife": "Knife",
    "Butterfly Knife": "Knife",
    "Classic Knife": "Knife",
    "Falchion Knife": "Knife",
    "Flip Knife": "Knife",
    "Gut Knife": "Knife",
    "Huntsman Knife": "Knife",
    "Karambit": "Knife",
    "Kukri Knife": "Knife",
    "M9 Bayonet": "Knife",
    "Navaja Knife": "Knife",
    "Nomad Knife": "Knife",
    "Paracord Knife": "Knife",
    "Shadow Daggers": "Knife",
    "Skeleton Knife": "Knife",
    "Stiletto Knife": "Knife",
    "Survival Knife": "Knife",
    "Talon Knife": "Knife",
    "Ursus Knife": "Knife",

    "Bloodhound Gloves": "Gloves",
    "Broken Fang Gloves": "Gloves",
    "Driver Gloves": "Gloves",
    "Hand Wraps": "Gloves",
    "Hydra Gloves": "Gloves",
    "Moto Gloves": "Gloves",
    "Specialist Gloves": "Gloves",
    "Sport Gloves": "Gloves",
}

# main target categories
CATEGORIES = [
    "Knife",
    "Gloves",
    "Pistol",
    "Rifle",
    "SMG",
    "heavy",
    "agent"
]

SKIN_PATTERN = re.compile(
    r"^(?P<weapon>.+?)"
    r"\s\|\s"
    r"(?P<skin>.+?)"
    r"\s\((?P<exterior>"
    r"Factory New|"
    r"Minimal Wear|"
    r"Field-Tested|"
    r"Well-Worn|"
    r"Battle-Scarred"
    r")\)$"
)

# Database Class that holds all query methods
class Database:
    def __init__(self,database_url: str):
        self.database_url = database_url
        self.table_names: list[str] = []

    # determines what category the incoming item is
    # We can use the market page attribute to get the item category
    # Ex) 'https://skinport.com/market/smg/ump-45?item=Primal%20Saber' - here we can extract the 'smg' part. 
    def get_cat(self,url):
        lowered_cat = [item.lower() for item in CATEGORIES]
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

    def update_item(self):
        pass

    def check_run(self):
            pass

    # insert into both skins and skin_prices
    def insert(self):
        conn = None
        cur = None

        try:
            conn = self.connect_to_database()
            cur = conn.cursor()
            data = sp.get_sp_json()

            # process each item that we got from the API
            for item in data:
                pass

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
    testdb.get_cat()
    # testdb.insert()

    # testdb.update_database()