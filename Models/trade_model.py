from config import get_db_connection, release_db_connection
import psycopg2.extras

class Trade():
      def create_transaction(self,transaction_id, user_id, token_name, order_type, trade_type, total_amount, price, token_amount):
            try:
                  conn = get_db_connection()
                  cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                  qry = "INSERT INTO transactions(txn_id,user_id, time, token_name, order_type, trade_type, total_amount, price, token_amount) VALUES (%s , %s, NOW() AT TIME ZONE 'Asia/Kolkata', %s, %s, %s, %s, %s, %s)"
                  values = (transaction_id, user_id, token_name, order_type, trade_type, total_amount, price, token_amount)
                  cursor.execute(qry, values)
                  conn.commit()
                  release_db_connection(conn)
                  return True
            except Exception as e:
                  print("Error in creating transaction", e)
                  if conn:
                        (release_db_connection(conn))
                        return 0
                  
      def get_trades(self, user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
            qry ="SELECT * FROM transactions WHERE user_id = %s"
            values = (user_id,)
            cursor.execute(qry, values)
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            cursor.close()
            release_db_connection(conn)
            if result:
                return result
            return 0
        except Exception as e:
            print("❌ Error getting trades:", e)
            if conn:
                release_db_connection(conn)
            return 0



    
