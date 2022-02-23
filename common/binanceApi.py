from dataclasses import dataclass, field

import requests
from binance.client import Client

try:
    from common.helpers import date_to_milliseconds
    from common.sensitive import BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY
except ImportError:
    from helpers import date_to_milliseconds
    from sensitive import BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY


def connect() -> Client:
    """Connect to binance"""
    i = 0
    while True:
        print(f"connecting{'.' * i}")
        try:
            client = Client(BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY)
            print(">>>Connected successfully to binance success")
            break

        except requests.exceptions.ConnectTimeout:
            i += 1

    return client


@dataclass
class BinanceClient:
    """Binance Client object"""

    client: Client = field(init=False, default=connect())

    def get_balance(self) -> dict:
        """Get the balance"""
        # hour_ago: int = date_to_milliseconds("1 second ago")
        nn = date_to_milliseconds("3 days ago")
        # nn = time.time()
        return self.client.get_account_status(
            timestamp=nn
        )  # , timestamp=nn, recvWindow=30000)["snapshotVos"][
        # "data"]
        # return self.client.get_all_coins_info()

    def get_timestamp(self):
        """get the server timestamp"""
        gt = self.client.get_server_time()
        # tt = time.gmtime(int((gt["serverTime"]) / 1000))

        return int((gt["serverTime"]))  # / 1000)
