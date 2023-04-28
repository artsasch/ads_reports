import pandas as pd
from utils import request


client_id = 1606473292  # ZOV
account_id = 1900012938
ids_type = 'client'
ids = '1606473292'
period = 'day'
date_from = '2023-03-01'
date_to = '0'


with open('access_token.txt', 'r') as file:
    access_token = file.read().strip()

ads_url = 'https://api.vk.com/method/ads.getStatistics'

ads_params = {
    'account_id': account_id,
    'access_token': access_token,
    'ids_type': ids_type,
    'ids': ids,
    'period': period,
    'date_from': date_from,
    'date_to': date_to,
    
    'v': '5.131'
}

ads_response_file = 'ads_response.json'

ads_response = request(ads_url, ads_params, ads_response_file)
df = pd.json_normalize(ads_response['response'][0]['stats'])

columns_to_drop = [
    "mobile_app_install_amount_by_interaction_time_postview",
    "mobile_app_install_amount_by_interaction_time_postclick",
    "mobile_app_install_amount_by_interaction_time_total",
    "mobile_app_install_amount_by_postback_time_postview",
    "mobile_app_install_amount_by_postback_time_postclick",
    "mobile_app_install_amount_by_postback_time_total",
    "mobile_app_install_cr_by_interaction_time_postview",
    "mobile_app_install_cr_by_interaction_time_postclick",
    "mobile_app_install_cr_by_interaction_time_total",
    "mobile_app_install_cr_by_postback_time_postview",
    "mobile_app_install_cr_by_postback_time_postclick",
    "mobile_app_install_cr_by_postback_time_total",
    "mobile_app_install_ecpa_by_interaction_time_postview",
    "mobile_app_install_ecpa_by_interaction_time_postclick",
    "mobile_app_install_ecpa_by_interaction_time_total",
    "mobile_app_install_ecpa_by_postback_time_postview",
    "mobile_app_install_ecpa_by_postback_time_postclick",
    "mobile_app_install_ecpa_by_postback_time_total"
]

df.drop(columns=columns_to_drop, inplace=True)
df.fillna(0, inplace=True)
df.to_csv('ads_response.csv', index=False)
