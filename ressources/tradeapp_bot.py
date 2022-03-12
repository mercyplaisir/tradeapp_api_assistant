"""

Tradeapp bot wrapper handling file
"""
from typing import Callable
from enum import Enum

from flask import request
from flask_restful import Resource

from common.utils import update_trading_history,set_new_data# set_status


class TradeappEndpoints(Enum):
    """
    tradeappbot  knows endpoints
    """
    STATUS = 'status'
    HISTORY = 'history'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
        
    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)


class TradeappModelHandler:
    """Handler this api model"""

    @classmethod
    def set_status(cls, req_data: dict):
        """set new status"""
        new_status = req_data['status']
        return set_new_data(new_status)

    @classmethod
    def append_history(cls, new_order: dict):
        """append the trading history"""
        if len(new_order) == 0:
            return None
        return update_trading_history(new_order)
    


class TradeappBotController(Resource):
    """Tradeapp Bot Flask's resource"""
    post_action: dict[str, Callable] = {
        'status': set_new_data,
        'history': update_trading_history,
        'profit': set_new_data,
        'error': set_new_data,
        'all': set_new_data
        # TlButtons.BALANCE: TradeappModel.balance
    }

    def post(self, message):
        runner: callable = self.post_action[message]
        data: dict = request.form  # ['data']
        return runner(data), 200
