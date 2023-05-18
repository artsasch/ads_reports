import requests
import json


agency_client_id = 15646746  # adv_green_vk


with open('.json/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data['adv_green_vk']['access_token']
print(access_token)

#
# url = 'https://ads.vk.com/api/v2/statistics/users/day.json'
# ad_group_id = 15646746
# date_from = '2023-01-01'
# date_to = '2023-05-13'
#
# params = {
#     'id': ad_group_id,
#     # 'date_from': date_from,
#     # 'date_to': date_to,
# }
#
# headers = {
#     'Authorization': f'Bearer {access_token}'
# }
#
# response = requests.get(url, params=params, headers=headers)
# data = response.json()
# with open('.json/base_data.json', 'w') as f:
#     json.dump(data, f)
