from flask import request,Blueprint,jsonify, make_response
from Models.users_model import UsersModel
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,unset_jwt_cookies
import datetime

obj = UsersModel()

users_controller = Blueprint('users_controller', __name__)

@users_controller.route('/', methods=['GET'])
def Home():
    return "Backend Is Running"

@users_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)

    user = obj.login(data)
    if user:
        token = create_access_token(identity=data["email"], expires_delta=datetime.timedelta(days=1))
        # ✅ Return the token in JSON instead of setting cookie
        print("Generated token:", token)
        return jsonify({
            "msg": "Login successful",
            "token": token
        }), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

    

@users_controller.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=1))
        # set token in cookie
        user = obj.register(username, name, email, password)
        if user:
            resp = make_response(jsonify({"msg": "User registered successfully"}))
            resp.set_cookie("access_token_cookie", token, httponly=True, samesite="Strict")
            return resp
        else:
            return jsonify({"msg": "Error: User not created"}), 400
        
@users_controller.route('/home', methods=['GET'])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Welcome {current_user}"})

@users_controller.route('/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({"msg": "Logout successful"}))
    resp.set_cookie(
        "access_token_cookie",
        "",
        httponly=True,
        samesite="Lax",
        secure=False,
        expires=0  # Expire the cookie immediately
    )
    return resp

@users_controller.route('/check-auth', methods=['GET'])
@jwt_required(locations=["cookies", "headers"])
def check_auth():
    try:
        current_user = get_jwt_identity()
        return jsonify({'authenticated': True, 'email': current_user}), 200
    except Exception as e:
        print("JWT error:", e)
        return jsonify({'authenticated': False}), 401