import psycopg
from config import DATABASE_URL

# Establish an abstracted connection
def get_connection():
    return psycopg.connect(DATABASE_URL)