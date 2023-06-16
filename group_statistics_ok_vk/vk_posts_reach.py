import datetime as dt
import pandas as pd
import requests
import json


with open('../resources/access_token.txt', 'r') as file:
    access_token = file.read().strip()

user_id = 689699902


response = requests.get('https://api.vk.com/method/stats.getPostReach',
                        params={
                            'access_token': access_token,
                            'owner_id': '-69145727',
                            'post_ids': '21253, 21247, 21244, 21238',
                            'v': '5.131'
                        }).json()

response = json.dumps(response, indent=3)
print(response)
