import requests


client_id = 51621899
client_secret = 'WBYfJpyRcOfrsuodGXAD'
url = 'https://ads.vk.com/api/v2/oauth2/token.json'

payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'permanent': 'true'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, params=payload, headers=headers)

print(response.json())
