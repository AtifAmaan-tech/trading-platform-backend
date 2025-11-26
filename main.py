import atexit
from flask import Flask, request, make_response
from flask_session import Session
from config import init_db_pool, close_db_pool
from dotenv import load_dotenv
import os
from datetime import timedelta
from Controller import controllers

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None' 
app.config['SESSION_COOKIE_SECURE'] = True 

# Create session directory if it doesn't exist
if not os.path.exists('./flask_session'):
    os.makedirs('./flask_session')

Session(app)
init_db_pool()

# Allowed origins - add your Render URL here after deployment
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://trading-platform-nu.vercel.app",
    "https://trading-platform-backend-1.onrender.com",
]

@app.before_request
def handle_cors_preflight():
    """Handle CORS preflight requests"""
    origin = request.headers.get('Origin')
    
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        if origin in ALLOWED_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = '86400'
        return response

@app.after_request
def add_cors_and_security_headers(response):
    """Add CORS headers to every response"""
    origin = request.headers.get('Origin')
    
    if origin in ALLOWED_ORIGINS:
        response.headers.pop('Access-Control-Allow-Origin', None)
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Vary'] = 'Origin'
    
    return response

# Register blueprints
for bp in controllers:
    app.register_blueprint(bp)

atexit.register(close_db_pool)

if __name__ == '__main__':
    # Use PORT environment variable for Render, default to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)  # debug=False for production