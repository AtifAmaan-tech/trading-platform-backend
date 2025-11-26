import atexit
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask
from flask_session import Session
from config import init_db_pool, close_db_pool
from dotenv import load_dotenv
import os
from datetime import timedelta
from Controller import controllers

load_dotenv()

app = Flask(__name__)
Session(app)
init_db_pool()

# --- CHANGE 1: Clean up CORS Origins ---
# Removed trailing slashes (e.g., .dev/) as they can sometimes cause matching issues
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:5173",
        "https://trading-platform-nu.vercel.app",
        "https://bioluminescent-deidre-dilative.ngrok-free.dev",
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True,
    "expose_headers": ["Content-Type"]
}})


app.secret_key = os.getenv("SECRET_KEY")

# --- CHANGE 2: CRITICAL SESSION FIX ---
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_HTTPONLY'] = True

# For Vercel -> Backend, you are Cross-Site. You MUST use 'None'.
app.config['SESSION_COOKIE_SAMESITE'] = 'None' 

# ERROR WAS HERE: Browsers REJECT SameSite='None' cookies if they are not Secure (HTTPS).
app.config['SESSION_COOKIE_SECURE'] = True 

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)


for bp in controllers:
    app.register_blueprint(bp)

atexit.register(close_db_pool)

if __name__ == '__main__':    
    app.run(host="0.0.0.0", port=5000, debug=True)