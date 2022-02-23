"""
Assistant api in the middle of the binance bot(backend) and the the telegram bot(frontend) 

"""

from flask import Flask
from flask_restful import Api

from ressources import (
    TelegramBot,
    TradeappBotController,
    CryptopairController,
    CoinController,
)

app = Flask(__name__)
api = Api(app)

# frontend endpoints


api.add_resource(TelegramBot, "/telegram/<string:message>")
api.add_resource(TradeappBotController, "/tradeapp/<string:message>")
api.add_resource(CryptopairController,"/cryptopair")
api.add_resource(CoinController,"/coin")


if __name__ == "__main__":
    app.run(debug=True)
