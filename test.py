from dataclasses import dataclass

import requests



order = {
    "symbol": "BNBBTC",
    "orderId": 28,
    "orderListId": -1,
    "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
    "transactTime": 1507725176595,
    "price": "0.00000000",
    "origQty": "10.00000000",
    "executedQty": "10.00000000",
    "cummulativeQuoteQty": "10.00000000",
    "status": "FILLED",
    "timeInForce": "GTC",
    "type": "MARKET",
    "side": "BUY"
}


@dataclass
class Order:
    """Binance Order Class"""

    # orderDetails : dict
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int
    price: str
    origQty: str
    executedQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str

    def dict(self):
        return self.__dict__

    def save(self):
        n = {}
        req = requests.post("http://127.0.0.1:5000/tradeapp/history", data=n)
        return req.json()


if __name__ == '__main__':
    url ="http://127.0.0.1:5000"
    endpoint = "/telegram/status"
    req = requests.get(url+endpoint)
    print(req.json())
