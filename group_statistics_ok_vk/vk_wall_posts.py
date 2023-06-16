import datetime as dt
import pandas as pd
import requests
import sqlalchemy
import json
from utils.utils import date_to_unix, unix_to_date, request


with open('../resources/access_token.txt', 'r') as file:
    access_token = file.read().strip()

user_id = 689699902

response = requests.get('https://api.vk.com/method/groups.get',
                        params={
                            'user_id': user_id,
                            'access_token': access_token,
                            'extended': 1,
                            'filter': 'moder',
                            'v': '5.131'
                        }).json()

groups = {}
for item in response['response']['items']:
    groups[item['id']] = item['screen_name']
    
# groups = {69145727: 'greenmarketby',
#           107352336: 'ostrov.chistoty',
#           40674131: 'savushkin_product',
#           89958692: 'zovofficial',
#           103458871: 'zefir_bel',
#           168145292: 'sportbeolarusofficial',
#           220826779: 'zoo.ostrov',
#           161701893: 'rabota_belagroprombank',
#           209182836: 'ostrov.zdorovya',
#           104556132: 'smmhero',
#           209388752: 'tri_losiya',
#           # 212950373: 'club212950373',
#           # 211650211: 'club211650211',
#           97749693: 'vokatv',
#           170611172: 'romax_factory',
#           137366127: 'nyxcosmeticskz', 
#           185023286: 'glowbyte',
#           126645970: 'lg_electronics_belarus',
#           127039209: 'minskworld',
#           211639056: 'art.estatedubai',
#           153050871: 'bgsby',
#           211116726: 'art.estatemsk',
#           143957632: '5s_agency',
#           203631808: 'flat_rent_brest',
#           109548042: 'verallyby',
#           66765464: 'lidkon',
#           208511747: 'mmk__by',
#           167047708: 'gomeldrevby'}

for group_id, group_shortname in groups.items():
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'domain': group_shortname,
                                'count': 100,
                                'access_token': access_token,
                                'v': '5.131'
                            }).json()
    group_shortname = group_shortname.replace(".", "_")
    try:
        items = response['response']['items']
        df = pd.json_normalize(items)
        df.drop('attachments', axis=1, inplace=True)
        df['date'] = pd.to_datetime(df['date'], unit='s')
        df = df.rename(columns=lambda x: x.replace('.', '_'))
        df.to_csv(f'assets_wall_posts_vk/{group_shortname}_wall_posts.csv', index=False)
    except Exception as e:
        print(f'error {e} in {group_shortname}')

    # try:
    #     engine = sqlalchemy.create_engine("mariadb+mariadbconnector://vk:yaro1997dobrg*M@173.249.18.74:3306/ads_reports")
    #     inspector = sqlalchemy.inspect(engine)
    #     table_name = f'{group_shortname}_wall_posts'
    #     if not inspector.has_table(table_name):
    #         df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)
    #     df.to_sql(table_name, engine, if_exists='replace', index=False)
    # except Exception as e:
    #     print(e)
    print(group_shortname)
