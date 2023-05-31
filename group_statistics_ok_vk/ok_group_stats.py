import requests
import json
import datetime
import pandas as pd
from utils_ok.utils import *


method = "url.getInfo"
url = "https://ok.ru/groupsavushkin"
getInfo_sig = md5_get_info(method, url)

params = {
    "application_key": application_key,
    "format": request_format,
    "method": method,
    "url": url,
    "sig": getInfo_sig,
    "access_token": access_token,
}

response = requests.get(api_url, params=params)
data = json.loads(response.text)
gid = data['objectId']
print(f"gid: {gid}")


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


start_time = "2023-04-01"
unix_start_time_ms = date_to_unix(start_time) * 1000

end_time = str(datetime.date.today())
unix_end_time_ms = date_to_unix(end_time) * 1000
print(f"start_time: {start_time}, end_time: {end_time}")
print(f"unix_start_time_ms: {unix_start_time_ms}, unix_end_time_ms: {unix_end_time_ms}")

getStatTrends_method = "group.getStatTrends"
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

for metric, values in data.items():
    for value in values:
        value["time"] = unix_to_date(value["time"] / 1000)

with open('utils_ok/response.json', 'w') as f:
    json.dump(data, f, indent=3)


df = pd.DataFrame()
for metric, values in data.items():
    metric_df = pd.DataFrame(values)
    metric_df.set_index('time', inplace=True)
    metric_df.rename(columns={'value': metric}, inplace=True)
    df = pd.concat([df, metric_df], axis=1)
df.reset_index(inplace=True)
print(df)
df.to_csv('utils_ok/response.csv', index=False)
