
from config import get_db_connection, release_db_connection
import psycopg2.extras

class UsersModel():
    def login(self, data):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            email = data.get("email")
            password = data.get("password")

            qry = "SELECT user_id, username, email, password FROM users WHERE email=%s AND password=%s"
            cursor.execute(qry, (email, password))
            user = cursor.fetchone()

            if user:
                # Return a clean dict of user info
                return {
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "email": user["email"],
                }
            else:
                return None
        except Exception as e:
            print("❌ Database Error (login):", e)
            return None
        finally:
            if conn:
                release_db_connection(conn)

    
    def register(self, username, name, email, password):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            qry = """
                INSERT INTO users (username, name, email, password)
                VALUES (%s, %s, %s, %s)
                RETURNING user_id, email
            """
            cursor.execute(qry, (username, name, email, password))
            conn.commit()

            user = cursor.fetchone()
            return {"user_id": user["user_id"], "email": user["email"]}

        except Exception as e:
            print("❌ Database Error (register):", e)
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                release_db_connection(conn)
    
    def get_user_by_email(self, email):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            qry = "SELECT user_id, username, email, password FROM users WHERE email = %s"
            cursor.execute(qry, (email,))
            user = cursor.fetchone()

            if user:
                return {
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "email": user["email"],
                    "password": user["password"]
                }
            else:
                return None
        except Exception as e:
            print("❌ Database Error (get_user_by_email):", e)
            return None
        finally:
            if conn:
                release_db_connection(conn)


    

