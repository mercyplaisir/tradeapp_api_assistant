"""

Tradeapp bot wrapper handling file
"""
from typing import Callable
from enum import Enum

from flask import request
from flask_restful import Resource

from common.utils import update_history, set_status


class TradeappButtons(Enum):
    """
    tradeapp endpoints
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


class ApiModel:
    """Handler this api model"""

    @classmethod
    def set_status(cls, req_data: dict):
        """set new status"""
        new_status = req_data['status']
        return set_status(new_status)

    @classmethod
    def append_history(cls, new_order: dict):
        """append the trading history"""
        if len(new_order) == 0:
            return None
        return update_history(new_order)


class TradeappBot(Resource):
    """Flask's resource"""
    bt_action: dict[str, Callable] = {
        TradeappButtons.STATUS: ApiModel.set_status,
        TradeappButtons.HISTORY: ApiModel.append_history
        # TlButtons.BALANCE: TradeappModel.balance
    }

    def post(self, message):
        runner: callable = self.bt_action[message]
        data: dict = request.form  # ['data']
        return runner(data), 200
