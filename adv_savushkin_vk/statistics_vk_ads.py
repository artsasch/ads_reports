import requests
import json
from datetime import datetime


with open('../resources/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data['adv_savushkin_vk']['access_token']

url = 'https://ads.vk.com/api/v2/statistics/users/day.json'
date_from = '2023-04-19'
date_to = datetime.now().strftime('%Y-%m-%d')

params = {
    'date_from': date_from,
    'date_to': date_to,
    'metrics': 'all'
}

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
with open('assets/base_statistics_vk.json', 'w') as f:
    json.dump(data, f, indent=3)
