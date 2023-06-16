import json
import pandas as pd
import requests


owner_id = 209388752

with open('../resources/access_token.txt', 'r') as file:
    access_token = file.read().strip()

response = requests.get('https://api.vk.com/method/wall.get',
                        params={
                            'owner_id': -owner_id,
                            'count': 100,
                            'access_token': access_token,
                            'v': '5.131'
                        }).json()
group_shortname = 'zovofficial'
try:
    items = response['response']['items']
    df_wall = pd.json_normalize(items)
    df_wall.drop('attachments', axis=1, inplace=True)
    df_wall['date'] = pd.to_datetime(df_wall['date'], unit='s')
    df_wall = df_wall.rename(columns=lambda x: x.replace('.', '_'))
except Exception as e:
    print(f'error 1 {e} in {group_shortname}')  


post_ids = df_wall['id'].tolist()
post_ids_arrays = [','.join(map(str, post_ids[i:i+30])) for i in range(0, len(post_ids), 30)]

response = requests.get('https://api.vk.com/method/stats.getPostReach',
                        params={
                            'access_token': access_token,
                            'owner_id': f'-{owner_id}',
                            'post_ids': post_ids_arrays[0],
                            'v': '5.131'
                        }).json()
response = json.dumps(response, indent=3)
print(response)
