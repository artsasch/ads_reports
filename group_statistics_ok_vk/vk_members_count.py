import pandas as pd
import requests
import datetime as dt
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
    groups[item['id']] = item['screen_name']

groups_ids = [key for key, value in groups.items()]
groups_ids_str = ', '.join(str(shortname) for shortname in groups_ids)

response = requests.get('https://api.vk.com/method/groups.getById',
                        params={
                            'access_token': access_token,
                            'group_ids': groups_ids_str,
                            'fields': 'name, screen_name, members_count',
                            'v': '5.131'
                        }).json()

df_members_count = pd.DataFrame(response['response'])
df_members_count = df_members_count.drop(['photo_50', 'photo_100', 'photo_200'], axis=1)
df_members_count.to_csv('member_counts.csv', index=False)


current_date = dt.date.today()
first_day_of_last_month = dt.date(current_date.year, current_date.month - 2, 1)
unix_timestamp_to, unix_timestamp_from = date_to_unix(str(current_date)), date_to_unix(str(first_day_of_last_month))
print(f"timestamp_to: {current_date} \ntimestamp_from: {first_day_of_last_month}")


for group_id, group_name in groups.items():

    members_count = df_members_count.loc[df_members_count['id'] == int(group_id), 'members_count'].values[0]

    url = 'https://api.vk.com/method/stats.get'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'timestamp_from': unix_timestamp_from,
        'timestamp_to': unix_timestamp_to,
        'interval': 'day',
        'v': '5.131'
    }

    group_name = f"{group_name}_stats_vk"
    response_json_file, response_csv_file = f'assets_vk/{group_name}.json', f'assets_vk/{group_name}.csv'

    try:
        response = request(url, params, response_json_file)
        df_stats = pd.json_normalize(response['response'])
        df_stats = df_stats.drop(['reach.age',
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
    except Exception as error:
        print(f'1 {error}, {group_name}')
        continue

    df_stats.loc[:, ['period_from', 'period_to']] = df_stats.loc[:, ['period_from', 'period_to']].apply(pd.to_datetime, unit='s')
    df_stats[['period_from', 'period_to']] = df_stats[['period_from', 'period_to']].apply(lambda x: x.dt.date)

    df_stats = df_stats.rename(columns=lambda x: x.replace('.', '_'))
    df_stats['members_count'] = 0
    df_stats.fillna(0, inplace=True)

    today = current_date - dt.timedelta(days=1)
    df_stats.loc[df_stats['period_from'] == today, 'members_count'] = members_count
    try:
        for i in range(1, len(df_stats)):
            members_count = members_count - df_stats.at[i, 'activity_subscribed'] + df_stats.at[i, 'activity_unsubscribed']
            df_stats.at[i, 'members_count'] = members_count
    except Exception as error:
        print(f'2 {error}, {group_name}')

    df_stats.to_csv(response_csv_file, index=False)
