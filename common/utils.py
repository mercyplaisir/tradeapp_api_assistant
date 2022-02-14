import csv
import json


def get_history() -> list[dict]:
    """return the trading history"""
    data = []
    # with open("../data/trades.csv", "r", newline='\n', encoding='utf-8') as csvfile:
    with open("data/trades.csv", "r", newline='\n', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # reader = csv.DictReader(csvfile)
        # print(json.dumps(reader))
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
