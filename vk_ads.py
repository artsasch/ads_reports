import datetime as dt
import pandas as pd
import requests


client_id = 1606473292  # ZOV
account_id = 1900012938
with open('access_token.txt', 'r') as file:
    access_token = file.read().strip()

url = 'https://api.vk.com/method/ads.getAds'

params = {
    'account_id': account_id,
    'client_id': client_id,
    'access_token': access_token,
    'v': '5.131'
}


# response = requests.get(url, params=params).json()
# print(response)

ads_url = 'https://api.vk.com/method/ads.getAccounts'

ads_params = {
    'access_token': access_token,
    'v': '5.131'
}


ads_response = requests.get(ads_url, params=ads_params).json()
print(ads_response)
# df = pd.json_normalize(response['response'])
# df.to_csv('vk_ads.csv', index=False)
