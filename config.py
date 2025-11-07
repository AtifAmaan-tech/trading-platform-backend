import psycopg2
import psycopg2.extras
from dotenv import load_dotenv 
import os
load_dotenv()

def get_db_connection():
    # Get the full connection string from Supabase
    conn_string = os.getenv("SUPABASE_CONNECTION_STRING")
    return psycopg2.connect(conn_string)

# conn = get_db_connection()
# cur = conn.cursor()
# cur.execute("SELECT * from Users")
# print(cur.fetchall())
# conn.close()