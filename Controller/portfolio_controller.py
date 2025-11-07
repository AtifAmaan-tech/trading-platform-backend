from flask import request,Blueprint,jsonify, make_response
from Models.users_model import UsersModel
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,unset_jwt_cookies
import datetime


obj = UsersModel()

users_controller = Blueprint('users_controller', __name__)

@users_controller.route('/portfolio', methods=['GET'])
def Portfolio():
    return "Portfolio Page"



