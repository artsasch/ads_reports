import requests
import datetime as dt
import pandas as pd
import json
import os.path


# https://oauth.vk.com/authorize?client_id=51621899&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,stats&response_type=token&v=5.131

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
df[['period_from', 'period_to']] = df[['period_from', 'period_to']].apply(lambda x: x.dt.strftime('%m/%d/%Y'))


df.to_csv('response.csv', index=False)

# days = len(response['response'])
# for i in range(3):
#     item = response['response'][i]
#     print(item['activity'])
#     print(f"period_from: {unix_to_date(item['period_from'])}")
#     print(f"period_to: {unix_to_date(item['period_to'])}")
#     print(f"reach/mobile_reach: {item['reach']['mobile_reach']}")
#     print(f"reach/reach: {item['reach']['reach']}")
#     print(f"reach/reach_subscribers: {item['reach']['reach_subscribers']}")
#     print(f"visitors/mobile_views: {item['visitors']['mobile_views']}")
#     print(f"visitors/views: {item['visitors']['views']}")
#     print(f"visitors/visitors: {item['visitors']['visitors']}")
#     print('////////////////////////////////////////////////////////////////')
# for i in range(days):
#     try:
#         subscribed = response['response'][i]['activity']['subscribed']
#         print(f'day: {i}, people subscribed: {subscribed}')
#     except Exception:
#         unsubscribed = response['response'][i]['activity']['unsubscribed']
#         print(f'day: {i}, people unsubscribed: {unsubscribed}')
