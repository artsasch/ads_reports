from datetime import datetime
import pandas as pd
import sqlalchemy
import requests
import json
import time


start_time = time.time()


def data_type_mapper(col):
    if col.dtype.name.startswith('int'):
        return pd.Int64Dtype()
    else:
        return float


accounts = ["adv_savushkin_mytarget",
            "adv_zov_vk",
            "adv_hr_belagroprombank_mytarget",
            "adv_green_mytarget",
            "adv_green_vk",
            "adv_belagroprombank_vk",
            "adv_savushkin_vk"]

with open('../resources/adv_tokens.json') as json_file:
    adv_tokens = json.load(json_file)

with open('../resources/mysql_engine.txt', 'r') as file:
    mysql_engine = file.read().strip()

url = 'https://ads.vk.com/api/v2/statistics/users/day.json'
date_from = '2023-04-01'
date_to = datetime.now().strftime('%Y-%m-%d')

params = {
    'date_from': date_from,
    'date_to': date_to,
    'metrics': 'all'
}

for account in accounts:
    access_token = adv_tokens[account]['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    with open(f'assets/{account}.json', 'w') as f:
        json.dump(data, f, indent=3)

    rows = data['items'][0]['rows']
    df = pd.json_normalize(rows)
    df = df.reset_index(drop=True)
    df = df.rename(columns=lambda x: x.replace('.', '_'))
    df.to_csv(f'assets/{account}.csv', index=False)
    date_column_name = 'date'

    df = df.apply(lambda col: col.astype(data_type_mapper(col)) if col.name != date_column_name else col)

    engine = sqlalchemy.create_engine(mysql_engine)
    inspector = sqlalchemy.inspect(engine)
    table_name = account

    if not inspector.has_table(table_name):
        df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)

    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"Data from {account} loaded.")


end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime} seconds")
