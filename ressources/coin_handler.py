"""For coin ressource hanlder"""
from flask_restful import Resource
from flask import request

from common import Coin


class CoinController(Resource):
    """Coin Flask's resource"""
    def get(self):
        """get all coin names"""
        return Coin.get_all_coins()
    def put(self):
        """update coin"""
    def post(self):
        """create new coin"""
        Coin.add()
    def delete(self):
        """delete coin"""
        # name = request.form['name']
        # Coin(name).delete()
        