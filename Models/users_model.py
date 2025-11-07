from config import get_db_connection
import psycopg2.extras

class UsersModel():
    def __init__(self):
        try:
            self.conn = get_db_connection()
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print("Database connected successfully")
        except Exception as e:
            print("Database connection error:", e)
            self.conn = None
            self.cursor = None

    def login(self,data):
        if not self.cursor:
            print("No database cursor available!")
            return None
        email = data.get("email")
        password = data.get("password")
        qry = "SELECT * FROM Users WHERE email=%s AND password=%s"
        values = (email, password)
        self.cursor.execute(qry, values)
        user = self.cursor.fetchone()
        return user
    
    def register(self,username, name, email, password):
        qry = "INSERT INTO Users(username,name,email,password) Values(%s,%s,%s,%s)"
        values = (username,name,email,password)
        self.cursor.execute(qry,values)
        self.conn.commit()  
        return True
    
    def get_user_by_email(self, email):
        qry = "SELECT * FROM Users WHERE email = %s"
        values = (email)
        self.cursor.execute(qry,values)
        row = self.cursor.fetchone()
        if row:
            return {"email":row[2],"password":row[3]}
        else:
            None


    

