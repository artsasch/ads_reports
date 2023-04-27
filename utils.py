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


def request(url, params):
    if os.path.isfile('response.json'):
        with open('response.json', 'r') as infile:
            response = json.load(infile)
            print("Loaded data from response.json file")
            return response
    else:
        response = requests.get(url, params=params).json()
    with open('response.json', 'w') as outfile:
        json.dump(response, outfile)
        print("Saved response to response.json file")
        return response
