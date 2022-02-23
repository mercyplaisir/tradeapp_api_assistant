import csv
import json

from decimal import Decimal
from typing import Union, Optional, Dict

import dateparser
import math
import pytz

from datetime import datetime
def get_history() -> list[dict]:
    """return the trading history"""
    data = []
    # with open("../data/trades.csv", "r", newline='\n', encoding='utf-8') as csvfile:
    with open("data/trades.csv", "r", newline='\n', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return json.dumps(data[1:])  # return data without the title(header)


def update_history(order: object) -> bool:
    """ Append the trading history"""
    with open("data/trades.csv", "a", newline='\n') as csvfile:
        fieldnames = list(order.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(order)
    return True


def get_status() -> dict[str, str]:
    """return the status"""
    # with open("../data/configuration.json", 'r') as jsonfile:
    with open("data/configuration.json", 'r') as jsonfile:
        reader: dict = json.load(jsonfile)
    return reader.pop('status')


def _get_config_file() -> dict:
    with open("data/configuration.json", 'r') as jsonfile:
        reader = json.load(jsonfile)
    return reader


def set_status(new_status: str) -> bool:
    """Set the new status"""
    data: dict = _get_config_file()
    data['status'] = new_status
    with open("data/configuration.json", 'w') as jsonfile:
        data_formated = json.dumps(data)
        jsonfile.write(data_formated)

    return True




#=================================================================================================
#=============== From helpers===============================================
#==================================================================




def date_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str, settings={'TIMEZONE': "UTC"})
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


def round_step_size(quantity: Union[float, Decimal], step_size: Union[float, Decimal]) -> float:
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
