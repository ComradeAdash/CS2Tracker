"""

seeding functions for initial data in item_categories, rarities, weapons, and exteriors tables

"""

def insert_categories(categories_list,cur):

    for category in categories_list:

        query = """
            INSERT INTO item_categories(name)
            VALUES (%s);
        """
    
        cur.execute(query,(category,))

def insert_weapons(weapons_dic,cur):

    for weapon,weapon_type in weapons_dic:
        query = """
                    INSERT INTO weapons (
                        name,
                        weapon_class
                    )
                    VALUES (%s, %s);
                """
        
        cur.execute(query,(weapon,weapon_type))

def insert_exterior(exteriors_dic,cur):

    for quality,order in exteriors_dic:
        query = """
                    INSERT INTO exteriors (
                        name,
                        quality_order
                    )
                    VALUES (%s, %s);
                """
        
        cur.execute(query,(quality,order))