import requests
import json

agency_client_id = 15646746  # adv_green_vk

with open('.json/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data[4]['adv_green_vk']['access_token']


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
