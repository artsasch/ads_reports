import hashlib
import datetime as dt
import os.path
import json
import requests


with open("utils_ok/access_token.txt", "r") as file:
    access_token = file.read().strip()

with open("utils_ok/application_key.txt", "r") as file:
    application_key = file.read().strip()
    
with open("utils_ok/session_secret_key.txt", "r") as file:
    session_secret_key = file.read().strip()

request_format = "json"
api_url = "https://api.ok.ru/fb.do"


def md5_get_info(method, url):
    string = f"application_key={application_key}format={request_format}method={method}url={url}{session_secret_key}"
    sig = hashlib.md5(string.encode("utf")).hexdigest()
    return sig


def md5_get_user_groups_v2(method):
    string = f"application_key={application_key}count=30format={request_format}method={method}{session_secret_key}"
    sig = hashlib.md5(string.encode("utf")).hexdigest()
    return sig


def md5_get_stat_trends(method, start_time, end_time, fields, gid):
    fields = fields.replace("\n", "").replace(" ", "")
    string = f"application_key={application_key}\
               end_time={end_time}\
               fields={fields}\
               format={request_format}\
               gid={gid}\
               method={method}\
               start_time={start_time}\
               {session_secret_key}"
    string = string.replace("\n", "").replace(" ", "")
    sig = hashlib.md5(string.encode("utf")).hexdigest()
    return sig


def unix_to_date(unix_timestamp):
    datetime = dt.datetime.fromtimestamp(unix_timestamp)
    date_timestamp = datetime.strftime("%Y-%m-%d")
    return date_timestamp


def date_to_unix(date_timestamp):
    datetime = dt.datetime.strptime(date_timestamp, "%Y-%m-%d")
    unix_timestamp = int(datetime.timestamp())
    return unix_timestamp


def request(url, params, response_file):
    if os.path.isfile(response_file):
        with open(response_file, 'r') as infile:
            response = json.load(infile)
            print(f"Loaded data from {response_file} file")
            return response
    else:
        response = requests.get(url, params=params).json()
    with open(response_file, 'w') as outfile:
        json.dump(response, outfile)
        print(f"Saved response to {response_file} file")
        return response
