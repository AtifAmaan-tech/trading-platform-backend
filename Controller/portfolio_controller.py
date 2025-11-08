from flask import request,Blueprint,jsonify,session
from Models.portfolio_model import Portfolio


obj = Portfolio()

portfolio_controller = Blueprint('portfolio_controller', __name__)

@portfolio_controller.route('/portfolio', methods=['GET'])
def Portfolio():
    return "Portfolio Page"



@portfolio_controller.route('/balance', methods=['GET'])
def balance():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"msg":"User not logged in"})
    
    balance = obj.get_balance(user_id)
    if balance is None:
        return jsonify({"msg": "Error fetching balance"}), 500
    
    return jsonify({
        "balance":balance
    }),200

