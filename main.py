from flask import Flask
from config import init_db_pool, close_db_pool
from dotenv import load_dotenv
import os
from datetime import timedelta
from Controller import controllers
load_dotenv()
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)

init_db_pool()

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type"]
    }
})

app.secret_key = os.getenv("SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # True in production with HTTPS
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

jwt = JWTManager(app)

for bp in controllers:
    app.register_blueprint(bp)

import atexit
atexit.register(close_db_pool)


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)