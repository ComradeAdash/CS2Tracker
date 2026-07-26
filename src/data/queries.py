"""

Query Methods to retieve and update database data

Notes: 


"""

import psycopg
import re
import config as cfg
import scripts.skin_port as sp

# Database Class that holds all query methods
class Database:
    def __init__(self,database_url: str):
        self.database_url = database_url
        self.table_names: list[str] = []

    # Creating a simple database connection
    def connect_to_database(self):
        try:
            return psycopg.connect(self.database_url)
        except Exception as error:
            print(error)

    # insert into both skins and skin_prices
    def insert():
        pass

    # Inserting / Updating the skins database with skin names and ids, assuming a connection is already open
    # A string like 'market_hash_name': 'UMP-45 | Primal Saber (Minimal Wear)' is parsed into
    # market_hash_name, weapon, skin_name, wear and inserted into 'skins'
    def insert_skin(self,cur,full_hash_name: str):
        # parse what we want
        separate= [
            value for value in re.split(r"[,| ()]+", full_hash_name)
            if value
        ]
        # insert market_hash_name, weapon, skin_name, wear
        insert_hash_data = ''' 
            INSERT INTO skins (
                market_hash_name,
                weapon,
                skin_name,
                wear
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (market_hash_name) DO NOTHING;
        '''
        cur.execute(insert_hash_data,full_hash_name, separate[0], separate[1], separate[2])
    
    # Updating the skin_prices database with the Skin-Port API data
    def insert_price(self):
        conn = None
        cur = None

        try:
            conn = self.connect_to_database()
            cur = conn.cursor()
            data = sp.get_sp_json()
        
            for item in data:
                #insert price data into skin_prices table
                insert_price_data = ''' 
                    INSERT INTO skin_prices (
                        market_hash_name,
                        weapon,
                        skin_name,
                        wear
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (market_hash_name) DO NOTHING;
                '''
                cur.execute(insert_price_data)
                pass
            
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

# Methods

# a simple function that tests our database connectivity
def test_bot():
    testdb = Database(cfg.DATABASE_URL)
    print(testdb.connect_to_database())


def run_bot():
    testdb = Database(cfg.DATABASE_URL)
    testdb.insert_skin("AK-47 | Asiimov (Well-Worn)")

    # testdb.update_database()