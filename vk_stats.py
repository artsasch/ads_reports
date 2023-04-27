import requests
import datetime as dt
import pandas as pd
import json
import os.path


# https://oauth.vk.com/authorize?client_id=51621899&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,stats,ads&response_type=code&v=5.131
# code = 500c5ab71de3cea21f
# https://oauth.vk.com/access_token?client_id=51621899&client_secret=WBYfJpyRcOfrsuodGXAD&redirect_uri=https://oauth.vk.com/blank.html&code=500c5ab71de3cea21f

def unix_to_date(unix_timestamp):
    datetime = dt.datetime.fromtimestamp(unix_timestamp)
    date_timestamp = datetime.strftime("%Y-%m-%d")
    return date_timestamp


def date_to_unix(date_timestamp):
    datetime = dt.datetime.strptime(date_timestamp, "%Y-%m-%d")
    unix_timestamp = int(datetime.timestamp())
    return unix_timestamp


current_date = dt.date.today()
first_day_of_last_month = dt.date(current_date.year, current_date.month-1, 1)

timestamp_from = f"{first_day_of_last_month:%Y-%m-%d}"
timestamp_to = f"{current_date:%Y-%m-%d}"

unix_timestamp_from = date_to_unix(timestamp_from)
unix_timestamp_to = date_to_unix(timestamp_to)

print(f"timestamp_from: {timestamp_from}")
print(f"timestamp_to: {timestamp_to}")


app_id = '51621899'
with open('access_token.txt', 'r') as file:
    access_token = file.read().strip()

url = 'https://api.vk.com/method/stats.get'

params = {
    'group_id': 69145727,  # Green
    'access_token': access_token,
    'timestamp_from': unix_timestamp_from,
    'timestamp_to': unix_timestamp_to,
    'interval': 'day',
    'v': '5.131'
}


if os.path.isfile('response.json'):
    with open('response.json', 'r') as infile:
        response = json.load(infile)
        print("Loaded data from response.json file")
else:
    response = requests.get(url, params=params).json()
    with open('response.json', 'w') as outfile:
        json.dump(response, outfile)
        print("Saved response to response.json file")


df = pd.json_normalize(response['response'])

df = df.drop(['reach.age',
              'reach.cities',
              'reach.countries',
              'reach.sex',
              'reach.sex_age',
              'visitors.age',
              'visitors.cities',
              'visitors.countries',
              'visitors.mobile_views',
              'visitors.sex',
              'visitors.sex_age'
              ], axis=1)


df.loc[:, ['period_from', 'period_to']] = df.loc[:, ['period_from', 'period_to']].apply(pd.to_datetime, unit='s')
df[['period_from', 'period_to']] = df[['period_from', 'period_to']].apply(lambda x: x.dt.date)


df.to_csv('response.csv', index=False)
