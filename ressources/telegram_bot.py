"""

Telegram bot handling file

"""
from typing import Callable

from flask_restful import Resource

from common.utils import get_history, get_status


# binance_client = BinanceClient() # binance client


# from common.binanceApi import BinanceClient


class TlButtons:
    HISTORY = 'history'
    BALANCE = 'balance'
    STATUS = 'status'


class TradeappModel:
    """Class wrapper that retrieve info of tradeapp model"""

    @classmethod
    def status(cls) -> str:
        return get_status()

    @classmethod
    def history(cls) -> list[dict]:
        return get_history()

    @classmethod
    def balance(cls):
        # return binance_client.get_balance
        pass


class TelegramBot(Resource):
    """Frontend access to binance Info"""

    # def get(self, message):  # , message):
    #     return binance_client.get_balance()
    bt_action: dict[str, Callable] = {
        TlButtons.STATUS: TradeappModel.status,
        TlButtons.HISTORY: TradeappModel.history,
        TlButtons.BALANCE: TradeappModel.balance
    }

    def get(self, message):
        runner: Callable = self.bt_action[message]
        return runner(), 200


if __name__ == '__main__':
    print(TlButtons.HISTORY)
