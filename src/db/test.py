import psycopg

conn = psycopg.connect(host="localhost", dbname="skinlemur",user="skinlemur",password="apple",port="5433")
cur = conn.cursor() 

# Creating our Database
cur.execute("""

CREATE TABLE IF NOT EXISTS skin_prices (
    id PRIMARY KEY,
    market_hash_name TEXT NOT NULL,
    min_price NUMERIC,
    max_price NUMERIC,
    mean_price NUMERIC,
    median_price NUMERIC,
    suggested_price NUMERIC,
    quantity INT
)

""")

conn.commit()
cur.close()
conn.close()