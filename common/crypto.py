"""for Cryptopair and Coin object representation"""



from dataclasses import dataclass
import datetime

import requests

# from common.dbcontroller import DbEngine
from dbcontroller import DbEngine


db = DbEngine()


class Coin(object):
    ...


@dataclass
class CryptoPair(object):
    """
    a representation of a cryptopair
    ex: BNBBTC
    """

    name: str
    database: object = db

    def __post_init__(self):
        self.verify()

    def verify(self):
        """Verify if the crypto pair really exits in the database"""

        nn = self.database.selectDB(
            f"select basecoin from relationalcoin where cryptopair='" + self.name + "'"
        )
        if len(nn) == 0:
            raise ValueError("the cryptopair doesn't exit in the database")

    @property
    def basecoin(self) -> Coin:
        """return a basecoin from a cryptopair
        ex: BNBBTC return BNB"""
        nn: list[tuple[str]] = self.database.selectDB(
            f"select basecoin from relationalcoin where cryptopair='" + self.name + "'"
        )

        name: str = nn[0][0]
        return Coin(name)

    @property
    def quotecoin(self) -> Coin:
        """return quotecoin from a cryptopair
        ex: BNBBTC return BTC"""
        nn = self.database.selectDB(
            f"select quotecoin from relationalcoin"
            + " where cryptopair='"
            + self.name
            + "'"
        )

        name: str = nn[0][0]
        return Coin(name)

    def is_basecoin(self, coin: Coin) -> bool:
        """return True if it iss a basecoin"""
        return self.name.startswith(coin.name)

    def is_quotecoin(self, coin: Coin) -> bool:
        """return True if it iss a quotecoin"""
        return self.name.endswith(coin.name)

    def is_any(self, coin: Coin):
        """To see if a coin is in the cryptopair"""
        if self.is_basecoin(coin) or self.is_quotecoin(coin):
            return True
        else:
            raise ValueError(f"{coin.name} is not in {self.name} ")
            return False

    def replace(self, coin: Coin) -> Coin:
        """return basecoin if the given coin is quotecoin vice-versa"""
        if self.is_basecoin(coin):
            return self.quotecoin
        elif self.is_quotecoin(coin):
            return self.basecoin
        else:
            raise ValueError(f"{coin.name} is not in {self.name} ")

    def get_price(self) -> float:
        """get price of a cryptopair"""
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={self.name}"
        resp = requests.get(url)
        return float(resp.json()["lastPrice"])

    def get_price_change(self) -> float:
        """gets priceChange of a crypto pair"""
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={self.name}"
        resp = requests.get(url)
        return float(resp.json()["priceChangePercent"])

    def delete(self):
        """
        :Delete a cryptopair
        :And by deleting the cryptopair it doesn't remove it's related coin
        """
        db.requestDB(f"delete from relationalcoin where cryptopair='{self.name}'")

    def __repr__(self) -> str:
        return self.name

    

    @classmethod
    def get_all_cryptopair(cls)->dict[str,str]:
        res = db.selectDB(" select cryptopair,basecoin,quotecoin from relationalcoin")
        data ={name: f'{bsc}-{qtc}' for name,bsc,qtc in res}
        return data


@dataclass
class Coin(object):
    """
    Representation of a Coin

    ex: BNB
    """

    name: str
    database: object = db

    def __post_init__(self):
        nn = self.database.selectDB(
            "select fullname from Coin where shortname='" + self.name + "'"
        )
        if len(nn) == 0:
            raise ValueError("the coin doens't exist in the database")

    @property
    def fullname(self):
        return self.database.selectDB(
            "select fullname from Coin where shortname='" + self.name + "'"
        )[0][0]

    def get_cryptopair_related(self) -> list[CryptoPair]:
        """return all coins related cryptopair where the coin appears to be a quotecoin or basecoin"""
        coin_name = self.name
        cryptopairs_name: list[tuple[str]] = self.database.selectDB(
            "select cryptopair from relationalcoin where basecoin ='"
            + coin_name
            + "' or quotecoin ='"
            + coin_name
            + "' "
        )
        return [CryptoPair(cryptopair_name[0]) for cryptopair_name in cryptopairs_name]

    def __repr__(self):
        return f"{self.name}({self.fullname})"
    
    def delete(self):
        """
        :Delete a coin
        :And by deleting the coin it delete all of it's cryptopair_related
        """
        #get all cryptopair
        cryptopairs = self.get_cryptopair_related()
        for cryptopair in cryptopairs:
            cryptopair.delete()

        db.requestDB(f"delete from Coin where shortname='{self.name}'")


    @classmethod
    def get_all_coins(cls):
        """get all coins"""
        res = db.selectDB("select shortname,fullname from Coin")
        
        return ({nume+1:name for nume,name in enumerate(res)})
        
    
if __name__=='__main__':
    res = db.selectDB("select shortname,fullname from Coin")

    print({nume+1:name for nume,name in enumerate(res) })
