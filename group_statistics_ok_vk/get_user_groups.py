import requests
import json
import datetime
import pandas as pd
from utils_ok.utils import *


get_user_groups_v2_method = "group.getUserGroupsV2"
get_user_groups_v2_sig = md5_get_user_groups_v2(get_user_groups_v2_method)

get_user_groups_v2_method_params = {
    "application_key": application_key,
    "count": 30,
    "format": request_format,
    "method": get_user_groups_v2_method,
    "sig": get_user_groups_v2_sig,
    "access_token": access_token,
}

response = requests.get(api_url, params=get_user_groups_v2_method_params)
data = json.loads(response.text)['groups']

uids = []
for i in data:
    uid = i['groupId']
    uids.append(uid)
uids = ",".join(uids)

get_group_info_method = "group.getInfo"
get_group_info_sig = md5_get_user_groups_v2(get_group_info_method)

get_group_info_method_params = {
    "application_key": application_key,
    "uids": uids,
    "fields": "shortname, uid",
    "format": request_format,
    "method": get_group_info_method,
    "sig": get_group_info_sig,
    "access_token": access_token,
}

response = requests.get(api_url, params=get_group_info_method_params)
data = json.loads(response.text)

shortnames = {}
for i in data:
    try:
        uid = i['uid']
        shortname = i['shortname']
        shortnames[uid] = shortname
    except KeyError as e:
        print(f"error {e} with {uid}")
print(shortnames)
