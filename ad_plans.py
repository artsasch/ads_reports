import requests
import json

agency_client_id = 15646713  # adv_zov_vk

with open('resources/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data['adv_zov_vk']['access_token']

url = 'https://ads.vk.com/api/v2/ad_plans.json'

params = {
    'id': agency_client_id,
    'metrics': 'all'
}

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, params=params, headers=headers)

print(response.json())
