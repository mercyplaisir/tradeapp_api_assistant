"""
Assistant api in the middle of the binance bot(backend) and the the telegram bot(frontend) 

"""

from flask import Flask, request
from common.utils import (
    get_all,
    order_restructure,
    set_new_data,
    update_trading_history,
    get_history,
    get_status,
    get_profit,
    get_error,
    order_restructure
)
import json


app = Flask(__name__)
# api = Api(app)


#===================GETTERS==============================
@app.route("/get/all", methods=["GET"])
def get_all_info():
    """return all data"""
    return json.dumps(get_all())


@app.route("/get/errors", methods=["GET"])
def get_errors():
    """return all data"""
    return json.dumps(get_error())


@app.route("/get/profit", methods=["GET"])
def profit():
    """return all data"""
    return json.dumps(get_profit())


@app.route("/get/status", methods=["GET"])
def status():
    """return all data"""
    return json.dumps(get_status())


@app.route("/get/orders", methods=["GET"])
def get_orders():
    """returns all orders"""
    orders = get_history()
    return json.dumps(order_restructure(orders))

@app.route("/hello", methods=["GET"])
def get_hello():
    """Hello word"""
    return json.dumps("Hello World")

#===========================SETTERS===================

@app.route("/set/all", methods=["POST"])
def set_data():
    """set new data"""
    req = request.form.to_dict()
    set_new_data(req)
    return json.dumps(f"succesfully append {req}")


@app.route("/set/order", methods=["POST"])
def append_order():
    """append new order"""
    req = request.form.to_dict()
    update_trading_history(req)
    return json.dumps(f"succesfully append order")




if __name__ == "__main__":
    app.run(debug=True)
