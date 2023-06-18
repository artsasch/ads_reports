from utils_ok.utils import *
import pandas as pd
import sqlalchemy
import datetime
import requests
import json


names = {'52958698209532': 'groupsavushkin',
         '55550518952020': 'greenmarketby',
         '55464149975040': 'vokatv',
         '52927256723523': 'ostrov.chistoty',
         '55790818296013': 'minskworld',
         '57587305152560': 'zefirby',
         '55712536133663': 'sportmaster.belarus',
         '53038939046008': 'apiok',
         '64096234766588': 'ostrov.zdorovya',
         '59188491518014': 'fabrikaromax',
         '64107739152636': 'tri.losya',
         '54213712019619': 'belgosstrakh',
         '53603784524025': 'lidkoncompany',
         '64827164524604': 'russkoe.more.official',
         '68669699784766': 'mmkby',
         '57719883038972': 'verallyby',
         '52108094341283': 'brestmeat'}

for uid, shortname in names.items():

    fields = "comments,\
              complaints, \
              content_opens, \
              engagement, \
              feedback, \
              hides_from_feed, \
              left_members, \
              likes, \
              link_clicks, \
              members_count, \
              members_diff, \
              music_plays, \
              negatives, \
              new_members, \
              new_members_target, \
              page_visits, \
              photo_opens, \
              reach, \
              reach_earned, \
              reach_mob, \
              reach_mobweb, \
              reach_own, \
              reach_web, \
              renderings, \
              reshares, \
              topic_opens, \
              video_plays, \
              votes"

    end_time = datetime.date.today()
    unix_end_time_ms = date_to_unix(str(end_time)) * 1000

    start_time = str(datetime.date(end_time.year, end_time.month - 2, 1))
    unix_start_time_ms = date_to_unix(start_time) * 1000

    getStatTrends_method = "group.getStatTrends"
    gid = uid
    sig = md5_get_stat_trends(getStatTrends_method, unix_start_time_ms, unix_end_time_ms, fields, gid)  # get sig

    group_params = {
        "application_key": application_key,
        "format": request_format,
        "method": getStatTrends_method,
        "gid": gid,
        "sig": sig,
        "access_token": access_token,
        "fields": fields,
        "start_time": unix_start_time_ms,
        "end_time": unix_end_time_ms
    }

    response = requests.get(api_url, params=group_params)
    data = json.loads(response.text)
    response_json_file = f'assets_ok/group_{shortname}_stats_ok.json'
    response_csv_file = f'assets_ok/group_{shortname}_stats_ok.csv'

    try:
        for metric, values in data.items():
            for value in values:
                value["time"] = unix_to_date(value["time"] / 1000)

        with open(response_json_file, 'w') as f:
            json.dump(data, f, indent=3)

        df = pd.DataFrame()
        for metric, values in data.items():
            metric_df = pd.DataFrame(values)
            metric_df.set_index('time', inplace=True)
            metric_df.rename(columns={'value': metric}, inplace=True)
            df = pd.concat([df, metric_df], axis=1)
        df.reset_index(inplace=True)
        df.to_csv(response_csv_file, index=False)

    except Exception as e:
        print(f"#{shortname}, {data['error_msg']}, {e}")

    engine = sqlalchemy.create_engine("mariadb+mariadbconnector://vk:yaro1997dobrg*M@173.249.18.74:3306/ads_reports")
    inspector = sqlalchemy.inspect(engine)
    table_name = f'group_{shortname}_stats_ok'

    if not inspector.has_table(table_name):
        df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)

    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'{table_name} loaded in database successfully')


print('done')


# url = f"https://ok.ru/{shortname}"
# method = "url.getInfo"
# getInfo_sig = md5_get_info(method, url)
#
# params = {
#     "application_key": application_key,
#     "format": request_format,
#     "method": method,
#     "url": url,
#     "sig": getInfo_sig,
#     "access_token": access_token,
# }
#
# response = requests.get(api_url, params=params)
# data = json.loads(response.text)
# gid = data['objectId']
# print(f"gid: {gid}")
