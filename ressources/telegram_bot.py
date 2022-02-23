"""

Telegram bot handling file

"""
from enum import Enum
from typing import Callable

from flask_restful import Resource

from common.utils import get_history, get_status





class TlEndpoints(Enum):
    """Telegram Buttons"""
    HISTORY = 'history'
    BALANCE = 'balance'
    STATUS = 'status'
    GET_ALL_COIN = 'all_crypto'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
        
    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)


class TradeappModel:
    """Class wrapper that retrieve info of tradeapp model"""

    @classmethod
    def status(cls) -> str:
        """get tradeappbot status"""
        return get_status()

    @classmethod
    def history(cls) -> list[dict]:
        """get the trading history"""
        return get_history()

    @classmethod
    def balance(cls):
        """get the balance
        # return binance_client.get_balance"""
        return
        
class TelegramBot(Resource):
    """Frontend access to binance Info"""

    # def get(self, message):  # , message):
    #     return binance_client.get_balance()
    bt_action: dict[str, Callable] = {
        TlEndpoints.STATUS: TradeappModel.status,
        TlEndpoints.HISTORY: TradeappModel.history,
        TlEndpoints.BALANCE: TradeappModel.balance
    }

    def get(self, message):
        """get method"""
        runner: Callable = self.bt_action[message]
        return runner(), 200


if __name__ == '__main__':
    print(TlEndpoints.HISTORY)
