import pandas as pd
import requests


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
print(groups)

groups_ids = [key for key, value in groups.items()]
groups_ids_str = ', '.join(str(shortname) for shortname in groups_ids)

response = requests.get('https://api.vk.com/method/groups.getById',
                        params={
                            'access_token': access_token,
                            'group_ids': groups_ids_str,
                            'fields': 'name, screen_name, members_count',
                            'v': '5.131'
                        }).json()

response_for_df_test = response
df = pd.DataFrame(response['response'])
print(df)

df.to_csv('assets_vk_members_count/member_counts.csv', index=False)
