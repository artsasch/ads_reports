import requests

app_id = '51617154'
access_rights = 'groups'
get_user_token_url = f'https://oauth.vk.com/authorize?client_id=${app_id}&scope=${access_rights}&response_type=token&v=5.131'

access = 'vk1.a.5E9SdzBdgN_uvH0YQTpVFw2VIXUb3XuFdXHDffgyw03dFlrQwfwwJGMgw0LP8grsEcIM5vzQAzI93n2qQ0mcyWLY8LM6HqQiqcFDJsvUtqGdewIPzyStshcibvYEdsRLZzADdIRGjT8q-sgLzJ_cNsvMd-DiQgHLGx-9nxhesNvfdWZD6PoJ9T_vh8UtrJrx8NbLd2I4hqQPbXWNzhocYQ'
access_account = 'vk1.a.y5K3AK4MTMCpMwUdTdb6FbVfjMYfkuooCdkW_paYU2lIjNz2NSxiGbiXSf8sx9nf8zPeuJtuWRecHZz_lOyfK4DKTyTMh-whZy_Vk2Ma_YwUpeZCLd01CJwBlTx0s3hBhtyjvtNyf4g7cU5lxApp5aTLnkDSQAyhPR05CwamMtOqk2zk3yD6zOSVw75khEVd'
access_groups = 'vk1.a.ZwcYEqHjWhqd_HusHUmM9L3SrOS8traQDsF9mhAVjca0DGVuvICTZj7Rq6d9HolxlZRq4EoFj9DGxzyIBPcznICwZSHwvTDalnvOhLyT9wSPbzU0RaAIk1l0OlIxhZHqc4gQDYOqlySwl9AAnYXvkPhgkCZPutIBa494QxwjlymoN4lLTglq5vUoySjUp3EvOfqr-Om5gb378m05singdA'
service_token = 'a9cfd9cda9cfd9cda9cfd9cd39aadc444faa9cfa9cfd9cdcdf3209f073509cd89de29ea'

url = 'https://api.vk.com/method/groups.get'

params = {
    'user_id': 140757512,
    'access_token': access_groups,
    'v': '5.131'
}

response = requests.get(url, params=params)

print(response.json())
