import requests
import json

# adv_zov_vk

with open('resources/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data['adv_zov_vk']['access_token']

url = 'https://ads.vk.com/api/v2/banners/138449156.json'

params = {
    'fields': 'id, name, textblocks'
}

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, params=params, headers=headers)

print(response.json())
