import requests
import json

agency_client_id = 13296456  # adv_savushkin_mytarget

with open('resources/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data['adv_savushkin_mytarget']['access_token']

url = 'https://ads.vk.com/api/v2/banners.json'

params = {
    'id': agency_client_id,
    'metrics': 'all'
}

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, params=params, headers=headers)

print(response.json())
