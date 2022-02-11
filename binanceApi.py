from dataclasses import dataclass, field

from binance.client import Client

from sensitive import BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY


def connect() -> Client:
    """Connect to binance """
    client = Client(BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY)
    print(">>>Connected successfully to binance success")
    return client


@dataclass
class BinanceClient:
    client: Client = field(init=False, default=connect())

    def get_balance(self) -> str:
        return self.client.get_account_snapshot(type="SPOT")["snapshotVos"]["data"]
    
