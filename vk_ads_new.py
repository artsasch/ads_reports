import requests


client_id = 51621899
client_secret = 'WBYfJpyRcOfrsuodGXAD'
agency_client_id = 15646713

url = 'https://ads.vk.com/api/v2/oauth2/token.json'

payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'agency_client_id': agency_client_id,
    'permanent': 'true'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, data=payload, headers=headers)

print(response.json())
