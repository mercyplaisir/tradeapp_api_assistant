"""for Coin Ressources and object implemntation"""

from flask_restful import Resource

from common import CryptoPair,Coin

class CryptopairController(Resource):
    """cryptopair Flask resource"""
    def __post_init__(self):
        """post init"""
         
    def get(self):
        """For getting all cryptopair"""
        cryptopairs:dict[str,str]= CryptoPair.get_all_cryptopair()
        return cryptopairs
    def post(self):
        """For creating cryptopair"""
    def put(self):
        """For updating cryptopair"""
    def delete(self):
        """For deleting cryptopair"""

