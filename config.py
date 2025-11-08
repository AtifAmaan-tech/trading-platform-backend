import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

load_dotenv()

# Create a global connection pool when your app starts
db_pool = None

def init_db_pool():
    """Initialize the connection pool once when the app starts."""
    global db_pool
    conn_string = os.getenv("SUPABASE_CONNECTION_STRING")

    if not conn_string:
        raise Exception("❌ SUPABASE_CONNECTION_STRING not found in .env")

    try:
        db_pool = pool.SimpleConnectionPool(
            minconn=1,   # Minimum number of open connections
            maxconn=10,  # Maximum number of open connections
            dsn=conn_string
        )
        print("✅ Database connection pool created successfully")
    except Exception as e:
        print("❌ Error creating database connection pool:", e)
        raise


def get_db_connection():
    """Get a connection from the pool."""
    global db_pool
    if db_pool is None:
        init_db_pool()
    return db_pool.getconn()


def release_db_connection(conn):
    """Return a connection back to the pool."""
    global db_pool
    if db_pool and conn:
        db_pool.putconn(conn)


def close_db_pool():
    """Close all pooled connections (useful on app shutdown)."""
    global db_pool
    if db_pool:
        db_pool.closeall()
        print("🧹 All database connections closed.")











# import psycopg2
# from dotenv import load_dotenv 
# import os
# load_dotenv()

# def get_db_connection():
#     # Get the full connection string from Supabase
#     conn_string = os.getenv("SUPABASE_CONNECTION_STRING")
#     return psycopg2.connect(conn_string)
