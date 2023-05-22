import datetime as dt
import pandas as pd
import sqlalchemy
from utils.utils import date_to_unix, unix_to_date, request


# https://oauth.vk.com/authorize?client_id=51621899&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,stats,ads&response_type=code&v=5.131
# code = 500c5ab71de3cea21f
# https://oauth.vk.com/access_token?client_id=51621899&client_secret=WBYfJpyRcOfrsuodGXAD&redirect_uri=https://oauth.vk.com/blank.html&code=500c5ab71de3cea21f


current_date = dt.date.today()
first_day_of_last_month = dt.date(current_date.year, current_date.month - 1, 1)

timestamp_from = f"{first_day_of_last_month:%Y-%m-%d}"
timestamp_to = f"{current_date:%Y-%m-%d}"

unix_timestamp_from = date_to_unix(timestamp_from)
unix_timestamp_to = date_to_unix(timestamp_to)

print(f"timestamp_from: {timestamp_from}")
print(f"timestamp_to: {timestamp_to}")


group_id = 40674131
with open('../resources/access_token.txt', 'r') as file:
    access_token = file.read().strip()

url = 'https://api.vk.com/method/stats.get'

params = {
    'group_id': group_id,
    'access_token': access_token,
    'timestamp_from': unix_timestamp_from,
    'timestamp_to': unix_timestamp_to,
    'interval': 'day',
    'v': '5.131'
}

response_json_file = 'assets/savushkin_vk_group_stats.json'
response_csv_file = 'assets/savushkin_vk_group_stats.csv'


response = request(url, params, response_json_file)
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

df = df.rename(columns=lambda x: x.replace('.', '_'))

df.fillna(0, inplace=True)
df.to_csv(response_csv_file, index=False)


# engine = sqlalchemy.create_engine("mariadb+mariadbconnector://vk:yaro1997dobrg*M@173.249.18.74:3306/vk_statistics")
# with engine.begin() as connection:
#     connection.execute('''TRUNCATE TABLE ''' + '''stats''')
#     df.to_sql('stats', con=connection, if_exists='append', index=bool)
# engine.dispose()
