import requests
import datetime as dt
import time


# https://oauth.vk.com/authorize?client_id=51621899&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,stats&response_type=token&v=5.131

def unix_to_date(unix_timestamp):
    datetime = dt.datetime.fromtimestamp(unix_timestamp)
    date_timestamp = datetime.strftime("%Y-%m-%d")
    return date_timestamp


def date_to_unix(date_timestamp):
    datetime = dt.datetime.strptime(date_timestamp, "%Y-%m-%d")
    unix_timestamp = int(datetime.timestamp())
    return unix_timestamp


app_id = '51621899'
with open('access_token.txt', 'r') as file:
    access_token = file.read().strip()

url = 'https://api.vk.com/method/stats.get'

params = {
    'group_id': 69145727,  # Green
    'access_token': access_token,
    'timestamp_from': 1680307200,
    'interval': 'week',
    'v': '5.131'
}

# response = requests.get(url, params=params)
# print(response.json())
