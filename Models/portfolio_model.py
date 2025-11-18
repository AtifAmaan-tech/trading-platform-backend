from config import get_db_connection, release_db_connection
import psycopg2.extras

class Portfolio():
    def get_balance(self, user_id):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            qry = "select token_balance from portfolio where user_id=%s AND token_symbol='USDT'"
            values = (user_id,)
            cursor.execute(qry,values)
            result = cursor.fetchone()
            cursor.close()
            release_db_connection(conn)
            print(result)
            if result:
                return result['token_balance']
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
            qry = "insert into portfolio (user_id, token_symbol, token_balance) values(%s,'USDT',%s)"
            values = (user_id,amount)
            cursor.execute(qry,values)
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
        

    def update_balance(self, amount, user_id, trade_type):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if trade_type == 'sell':
                qry = "UPDATE portfolio SET token_balance = token_balance + %s WHERE user_id=%s AND token_symbol='USDT'"
            else:
                qry = "UPDATE portfolio SET token_balance = token_balance - %s WHERE user_id=%s AND token_symbol='USDT'"
            print(qry)
            values = (amount, user_id)
            print("Amount:", amount)
            print("User ID:", user_id)
            print("Trade Type:", trade_type)
            cursor.execute(qry, values)
            print("Rows affected:", cursor.rowcount)
            conn.commit()
            cursor.close()
            release_db_connection(conn)
            return True
        except Exception as e:
            print("❌Error in updating balance", e)
            if conn:
                release_db_connection(conn)
            return 0
        
    def add_token(self, user_id, token_symbol, quantity, token_price):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            token_balance = quantity * token_price

            qry = """
            INSERT INTO portfolio (user_id, token_symbol, quantity, token_balance)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, token_symbol)
            DO UPDATE SET
                quantity = portfolio.quantity + EXCLUDED.quantity,
                token_balance = portfolio.token_balance + EXCLUDED.token_balance;
            """
            values = (user_id, token_symbol, quantity, token_balance)
            cursor.execute(qry, values)
            conn.commit()
            cursor.close()
            release_db_connection(conn)
            return True

        except Exception as e:
            print("❌ Error in updating balance:", e)
            if conn:
                release_db_connection(conn)
            return 0
        
    def get_tokens_qty(self, user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
            qry = "SELECT token_symbol,quantity FROM portfolio WHERE user_id = %s"
            values = (user_id,)
            cursor.execute(qry, values)
            result = cursor.fetchall()
            cursor.close()
            release_db_connection(conn)
            return result
        except Exception as e:
            print("Error geting tokens quantity", e)
            if conn:
                release_db_connection(conn)
            return 0


