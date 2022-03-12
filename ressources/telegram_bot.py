"""

Telegram bot handling file

"""
from enum import Enum
from typing import Callable

from flask_restful import Resource

from common.utils import get_history, get_status,get_all,get_error,get_profit





    
        
class TelegramBot(Resource):
    """Frontend access to binance Info"""

    # def get(self, message):  # , message):
    #     return binance_client.get_balance()
    bt_action: dict[str, Callable] = {
        'status': get_status,
        'history': get_history,
        'all': get_all,
        'error': get_error,
        'profit': get_profit
    }

    def get(self, message):
        """get method"""
        runner: Callable = self.bt_action[message]
        return runner(), 200


if __name__ == '__main__':
    """"""
    # print(TlEndpoints.HISTORY)
