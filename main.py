from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

binance_endpoint = "/binance"


class BinanceClient(Resource):
    def get(self):
        return {"data": "hello word"}


api.add_resource(BinanceClient, binance_endpoint)

if __name__ == '__main__':
    app.run(debug=True)
