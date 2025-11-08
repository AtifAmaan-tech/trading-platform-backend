from config import get_db_connection, release_db_connection
import psycopg2.extras

class Portfolio():
    def get_balance(self, user_id):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            qry = "select balance from portfolio where user_id=%s"
            values = (user_id,)
            cursor.execute(qry,values)
            result = cursor.fetchone()
            cursor.close()
            release_db_connection(conn)
            print(result)
            if result:
                return result['balance']
            return 0
        except Exception as e:
            print("❌ Database Error:", e)
            if conn:
                release_db_connection(conn)
            return 0
        
    
    def add_balance(self, user_id,amount):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            qry = "insert into portfolio (user_id, balance) values(%s,%s)"
            values = (user_id,amount)
            cursor.execute(qry,values)
            print("🟡 Running Query:", qry, values)
            conn.commit()
            cursor.close()
            release_db_connection(conn)
            print("✅ Balance added for user_id:", user_id)
            return True
        except Exception as e:
            print("❌ Database Error (add_balance):", e)
            if conn:
                release_db_connection(conn)
            return 0

