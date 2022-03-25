import csv
import json

from decimal import Decimal
from typing import Union, Optional, Dict

import dateparser
import math
import pytz

# filenames
trades_file = "data/trades.csv"
config_file = "data/configuration.json"

from datetime import datetime


def get_history() -> list[list]:
    """return the trading history"""
    data = read_csv_file()
    return data


def update_trading_history(data: dict) -> bool:
    """Append the trading history"""
    append_dict_in_csv(trades_file, data)


def get_status() -> dict[str, str]:
    """return the status"""
    data = get_config_file()
    return data.pop("status")


def get_error():
    data = get_config_file()
    cleaned_data = dict_to_string(data["errors"])
    return cleaned_data


def get_profit():
    data: dict = load_from_json_file(config_file)
    return data.pop("profit")


def get_config_file() -> dict:
    data: dict = load_from_json_file(config_file)
    return data


def get_all():
    data: dict = load_from_json_file(config_file)
    return dict_to_string(data)


def set_new_data(new_data: dict) -> bool:
    """Set the new status"""
    data: dict = get_config_file()
    data.update(new_data)
    write_in_json_file(config_file, data)


# =================================================================================================
# =============== From helpers===============================================
# ==================================================================


def read_csv_file():
    data = []
    with open(trades_file, "r", newline="\n", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data[1:]  # return data without the title(header)


def load_from_json_file(path):
    with open(path, "r") as f:
        loaded_data = json.load(f)
    return loaded_data


def write_in_json_file(path, data):
    with open(path, "w") as f:
        formatted_data = json.dumps(data)
        f.write(formatted_data)


def append_dict_in_csv(path, data, newline="\n"):
    assert isinstance(data, dict), "must be a dict"
    with open(trades_file, "a", newline=newline) as csvfile:
        fieldnames = list(data.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)


def date_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str, settings={"TIMEZONE": "UTC"})
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval: str) -> Optional[int]:
    """Convert a Binance interval string to milliseconds

    :param interval: Binance interval string, e.g.: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w

    :return:
         int value of interval in milliseconds
         None if interval prefix is not a decimal integer
         None if interval suffix is not one of m, h, d, w

    """
    seconds_per_unit: Dict[str, int] = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
    }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None


def round_step_size(
    quantity: Union[float, Decimal], step_size: Union[float, Decimal]
) -> float:
    """Rounds a given quantity to a specific step size

    :param quantity: required
    :param step_size: required

    :return: decimal
    """
    precision: int = int(round(-math.log(step_size, 10), 0))
    return float(round(quantity, precision))


def convert_ts_str(ts_str):
    if ts_str is None:
        return ts_str
    if type(ts_str) == int:
        return ts_str
    return date_to_milliseconds(ts_str)


def dict_to_string(d: dict, issubdict=False, level=0):
    """change a string to a well formatted string"""

    assert isinstance(d, dict), "must be a type dictionary"
    assert len(d) > 0, "the given dictionnary is empty"
    dict_items = d.items()
    formatted_string = ""
    level = level  # level of the dict

    if issubdict:
        formatted_string = "\n" + formatted_string
    for key, value in dict_items:
        if isinstance(value, dict):
            new_level = level + 1
            value = dict_to_string(value, level=new_level, issubdict=True)
        if issubdict:
            nn = "\t" * level
            formatted_string += f"{nn}{key} : {value} \n"
        else:
            formatted_string += f"{key} : {value} \n"

    return formatted_string


# ===================================
def _order_format(order):
    if len(order) == 0:
        return ""
    (
        symbol,
        orderId,
        orderListId,
        clientOrderId,
        transactTime,
        price,
        origQty,
        executedQty,
        cummulativeQuoteQty,
        status,
        timeInForce,
        order_type,
        side,
    ) = order

    transactTime = str(datetime.fromtimestamp(float(float(order[4]) / 1000)))[:-4] +' '+ timeInForce   
    data = [symbol,side,price,executedQty,transactTime]
    return " | ".join(data)
    # return  f'{cryptopair} |   {tt}  |   {order_type}   | \n '


def order_restructure(orders):
    result = "symbol | type | price | quantity | time"
    for order in orders:
        # print(len(order))
        result +=' \n'
        result += _order_format(order)
    return result
