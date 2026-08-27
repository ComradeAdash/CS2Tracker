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

WEAPON_CATEGORIES = {

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

    # Creating a simple database connection
    def connect_to_database(self):
        try:
            return psycopg.connect(self.database_url)
        except Exception as error:
            print(error)

    # insert into both skins and skin_prices
    def insert(self):
        conn = None
        cur = None

        try:
            conn = self.connect_to_database()
            cur = conn.cursor()
            data = sp.get_sp_json()

            for item in data:
                self.insert_price(cur,item)

            conn.commit()
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    # Inserting / Updating the skins database with skin names and ids, assuming a connection is already open
    # A string like 'market_hash_name': 'UMP-45 | Primal Saber (Minimal Wear)' is parsed into
    # market_hash_name, weapon, skin_name, wear and inserted into the respective Knife, Glove, Case, Weaopon, Sticker table. 
    def insert_skin(self,cur,full_hash_name: str):
        separate = [
            value for value in re.split(r"[,| ()]+", full_hash_name)
            if value
        ]
        
        # Need to insert into the correct table
        
        
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
        cur.execute(insert_hash_data, (full_hash_name, separate[0], separate[1], separate[2]))
    
    # Updating the skin_prices database with the Skin-Port API data
    def insert_price(self,cur,item):
        #insert price data into skin_prices table
        insert_price_data = ''' 
            INSERT INTO skin_prices (
                market_hash_name,
                source,
                currency,
                min_price,
                max_price,
                mean_price,
                median_price,
                suggested_price,
                quantity
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (
            item['market_hash_name'],"Skin-Port",item['currency'],
            item['min_price'],item['max_price'],item['mean_price'],
            item['median_price'],item['suggested_price'],item['quantity']
        )
        cur.execute(insert_price_data,params)
            

# Methods

# a simple function that tests our database connectivity
def test_conn():
    testdb = Database(cfg.DATABASE_URL)
    print(testdb.connect_to_database())


def run_bot():
    testdb = Database(cfg.DATABASE_URL)
    testdb.insert()

    # testdb.update_database()