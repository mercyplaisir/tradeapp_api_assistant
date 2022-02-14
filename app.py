"""
Assistant api in the middle of the binance bot(backend) and the the telegram bot(frontend) 

"""

from flask import Flask
from flask_restful import Api

from ressources.telegram_bot import TelegramBot
from ressources.tradeapp_bot import TradeappBot

app = Flask(__name__)
api = Api(app)

# frontend endpoints
telegram_bot = {
    "get": "/frontend/<str>",  # get trade history

}
post_binance = "/binance/<string:message>"

api.add_resource(TelegramBot,
                 '/telegram/<string:message>')
api.add_resource(TradeappBot,
                 '/tradeapp/<string:message>')

if __name__ == '__main__':
    app.run(debug=True)
