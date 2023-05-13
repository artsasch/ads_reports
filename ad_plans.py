import requests


with open('utils/vk_ads_new_access_token.txt', 'r') as file:
    access_token = file.read().strip()

url = 'https://ads.vk.com/api/v2/ad_plans.json'
ad_group_id = 15646746

params = {
    'id': ad_group_id,
    'metrics': 'all'
}

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, params=params, headers=headers)

print(response.json())
