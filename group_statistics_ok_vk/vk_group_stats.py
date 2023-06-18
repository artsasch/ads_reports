import datetime as dt
import pandas as pd
import requests
import sqlalchemy
from utils_vk.utils import date_to_unix, unix_to_date, request


with open('../resources/access_token.txt', 'r') as file:
    access_token = file.read().strip()

user_id = 689699902

response = requests.get('https://api.vk.com/method/groups.get',
                        params={
                                'user_id': user_id,
                                'access_token': access_token,
                                'extended': 1,
                                'filter': 'moder',
                                'v': '5.131'
                        }).json()

groups = {}
for item in response['response']['items']:
    groups[item['screen_name']] = item['id']


current_date = dt.date.today()
first_day_of_last_month = dt.date(current_date.year, current_date.month - 2, 1)
unix_timestamp_to = date_to_unix(str(current_date))
unix_timestamp_from = date_to_unix(str(first_day_of_last_month))
print(f"timestamp_to: {current_date}")
print(f"timestamp_from: {first_day_of_last_month}")


for group_name, group_id in groups.items():

    url = 'https://api.vk.com/method/stats.get'

    params = {
        'group_id': group_id,
        'access_token': access_token,
        'timestamp_from': unix_timestamp_from,
        'timestamp_to': unix_timestamp_to,
        'interval': 'day',
        'v': '5.131'
    }

    group_name = f"group_{group_name}_stats_vk"
    response_json_file = f'assets/{group_name}.json'
    response_csv_file = f'assets/{group_name}.csv'

    try:
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
    except KeyError as error:
        print(error, group_name, group_id)
        continue
    except:
        print(f"error in group{group_name}")
        continue

    df.loc[:, ['period_from', 'period_to']] = df.loc[:, ['period_from', 'period_to']].apply(pd.to_datetime, unit='s')
    df[['period_from', 'period_to']] = df[['period_from', 'period_to']].apply(lambda x: x.dt.date)

    df = df.rename(columns=lambda x: x.replace('.', '_'))

    df.fillna(0, inplace=True)
    df.to_csv(response_csv_file, index=False)

    # engine = sqlalchemy.create_engine("mariadb+mariadbconnector://vk:yaro1997dobrg*M@173.249.18.74:3306/ads_reports")
    # inspector = sqlalchemy.inspect(engine)
    # table_name = group_name
    # print(table_name)
    #
    # if not inspector.has_table(table_name):
    #     df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)
    #
    # df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'{group_name} loaded in database successfully')

print("done")


# https://oauth.vk.com/authorize?client_id=51621899&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,stats,ads,wall&response_type=code&v=5.131
# code = "500c5ab71de3cea21f"
# https://oauth.vk.com/access_token?client_id=51621899&client_secret=WBYfJpyRcOfrsuodGXAD&redirect_uri=https://oauth.vk.com/blank.html&code=906a45541003af96fd
