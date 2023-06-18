import datetime as dt
import os.path
import json
import requests


def unix_to_date(unix_timestamp):
    datetime = dt.datetime.fromtimestamp(unix_timestamp)
    date_timestamp = datetime.strftime("%Y-%m-%d")
    return date_timestamp


def date_to_unix(date_timestamp):
    datetime = dt.datetime.strptime(date_timestamp, "%Y-%m-%d")
    unix_timestamp = int(datetime.timestamp())
    return unix_timestamp


def request(url, params, response_file):
    response = requests.get(url, params=params).json()
    with open(response_file, 'w') as outfile:
        json.dump(response, outfile)
        return response
