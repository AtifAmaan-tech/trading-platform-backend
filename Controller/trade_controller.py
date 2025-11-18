from flask import request,Blueprint,jsonify,session
from Models.trade_model import Trade
from Models.portfolio_model import Portfolio
import random


obj = Trade()
portfolio_obj = Portfolio()

trade_controller = Blueprint('trade_controller', __name__)

@trade_controller.route('/trade', methods=['GET'])
def Trade():
    return "Trade Page"

@trade_controller.route("/create-transaction", methods=['POST'])
def create_transaction():
    for _ in range(5):
        try:
            transaction_id = random.randint( 10**5,10**6-1)
            print(transaction_id)
            user_id = session['user_id']
            token_name = request.json.get("data", {}).get("crypto")
            order_type = request.json.get("data", {}).get("orderType")
            trade_type = request.json.get("data", {}).get("tradeType")
            token_amount = request.json.get("data", {}).get("amount")
            total_amount = request.json.get("data", {}).get("total")
            price = request.json.get("data", {}).get("price")
            print("total amount: ", total_amount)
            obj.create_transaction(transaction_id, user_id, token_name, order_type, trade_type, total_amount, price, token_amount)
            portfolio_obj.update_balance(total_amount, user_id, trade_type)

            portfolio_obj.add_token(user_id, token_name, token_amount, price)
            return jsonify({"msg": "Transaction Created Successfully"}),200
        except Exception as e:
            print(e) 
            continue
    return jsonify({"error": "Failed to create unique transaction ID"}), 500


@trade_controller.route("/get_trades", methods=['GET'])
def get_trades():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"msg":"User not logged in"})
        print(user_id)
        trades = obj.get_trades(user_id)
        return jsonify({"trades":trades}),200

    except Exception as e:
        print(e)


