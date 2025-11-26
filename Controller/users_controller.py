from flask import request,Blueprint,jsonify, make_response,session
from Models.users_model import UsersModel
from Models.portfolio_model import Portfolio

obj = UsersModel()
portfolio_obj = Portfolio()
users_controller = Blueprint('users_controller', __name__)

@users_controller.route('/', methods=['GET'])
def Home():
    return "Backend Is Running"

@users_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = obj.login(data)
    print(data)
    if user:
        session.permanent = True
        session['user_id'] = user['user_id']
        session['email'] = user['email']
        print(session.get('user_id'))
        print("Login Successful !")
        return jsonify({
            "msg": "Login successful",
            "user_id": user['user_id']
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

    

@users_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    user = obj.register(username, name, email, password)
    
    if user:
        # Store user info in session
        session.permanent = True
        session['user_id'] = user['user_id']   # store the id of created user
        session['email'] = user['email']  

        portfolio_obj.add_balance(user['user_id'],1000)

        print(f"✅ Session created: user_id={session['user_id']}, email={session['email']}")  # Debug

        return jsonify({
            "msg": "User registered successfully",
            "user_id": user['user_id']
        }), 200
    else:
        return jsonify({"msg": "Error: User not created"}), 400
        
@users_controller.route('/home', methods=['GET'])
def home():
    return jsonify({"msg": f"Welcome!"})

@users_controller.route('/logout', methods=['POST'])
def logout():
    print("Before clear:", dict(session))
    session.clear()
    print("After clear:", dict(session))
    resp = make_response(jsonify({"msg": "Logout successful"}))
    resp.set_cookie(
    'session', 
    '', 
    expires=0, 
    path='/', 
    httponly=True, 
    secure=False,  # or True if using HTTPS
    samesite='Lax'
)
    return resp


@users_controller.route('/auth-status', methods=['GET'])
def auth_status():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({
            "logged_in": True,
            "user_id": user_id,
            "email": session.get('email')
        }), 200
    else:
        return jsonify({"logged_in": False}), 500
