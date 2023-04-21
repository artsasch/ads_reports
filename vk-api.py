import requests


# https://oauth.vk.com/authorize?client_id=51621899&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,stats&response_type=token&v=5.131

app_id = '51621899'
with open('access_token.txt', 'r') as file:
    access_token = file.read().strip()

url = 'https://api.vk.com/method/stats.get'

params = {
    'group_id': 69145727,
    'app_id': app_id,
    'access_token': access_token,
    'timestamp_from': 1680307200,
    'interval': 'week',
    'v': '5.131'
}

response = requests.get(url, params=params)
print(response.json())
