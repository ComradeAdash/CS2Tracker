"""

Script to seed the database with initial values for item_categories, weapons, and exteriors

"""

import data.setup as ds
import data.queries as queries
import config as cfg
import traceback

categories_list = cfg.CATEGORIES
weapons_dic = cfg.WEAPON_TYPES
exteriors_dic = cfg.EXTERIOR_ORDER

try:
    db = queries.Database(cfg.DATABASE_URL)
    conn = db.connect_to_database()
    cur = conn.cursor()

    # seed the data

    ds.insert_categories(cfg.CATEGORIES,cur)
    ds.insert_weapons(cfg.WEAPON_TYPES.items(),cur)
    ds.insert_exterior(cfg.EXTERIOR_ORDER.items(),cur)

    conn.commit()

except Exception as error:
            print(error)
            traceback.print_exc()
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()