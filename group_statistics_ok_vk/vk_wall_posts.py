import datetime as dt
import pandas as pd
import requests
import sqlalchemy
import json
from utils_vk.utils import date_to_unix, unix_to_date, request


with open('../resources/access_token.txt', 'r') as file:
    access_token = file.read().strip()

user_id = 689699902

# response = requests.get('https://api.vk.com/method/groups.get',
#                         params={
#                             'user_id': user_id,
#                             'access_token': access_token,
#                             'extended': 1,
#                             'filter': 'moder',
#                             'v': '5.131'
#                         }).json()
#
# groups = {}
# for item in response['response']['items']:
#     groups[item['id']] = item['screen_name']

groups = {69145727: 'greenmarketby',
          107352336: 'ostrov.chistoty',
          40674131: 'savushkin_product',
          89958692: 'zovofficial',
          103458871: 'zefir_bel',
          168145292: 'sportbeolarusofficial',
          # 220826779: 'zoo.ostrov',  # No access
          161701893: 'rabota_belagroprombank',
          # 209182836: 'ostrov.zdorovya',  # No access
          # 209388752: 'tri_losiya',  # No access
          97749693: 'vokatv',
          170611172: 'romax_factory',
          137366127: 'nyxcosmeticskz',
          185023286: 'glowbyte',
          126645970: 'lg_electronics_belarus',
          127039209: 'minskworld',
          211639056: 'art.estatedubai',
          153050871: 'bgsby',
          211116726: 'art.estatemsk',
          # 143957632: '5s_agency',
          203631808: 'flat_rent_brest',
          109548042: 'verallyby',
          66765464: 'lidkon',
          208511747: 'mmk__by',
          167047708: 'gomeldrevby'}

for group_id, group_shortname in groups.items():
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'owner_id': -group_id,
                                'count': 100,
                                'access_token': access_token,
                                'v': '5.131'
                            }).json()
    group_shortname = group_shortname.replace(".", "_")
    try:
        items = response['response']['items']
        df_wall = pd.json_normalize(items)
        df_wall.drop('attachments', axis=1, inplace=True)
        df_wall['date'] = pd.to_datetime(df_wall['date'], unit='s')
        df_wall = df_wall.rename(columns=lambda x: x.replace('.', '_'))
        post_ids = df_wall['id'].tolist()
        post_ids_arrays = [','.join(map(str, post_ids[i:i+30])) for i in range(0, len(post_ids), 30)]
    except Exception as e:
        print(f'error 1 {e} in {group_shortname}')

    df_posts = pd.DataFrame()

    for post_ids in post_ids_arrays:
        try:
            response = requests.get('https://api.vk.com/method/stats.getPostReach',
                                    params={
                                        'access_token': access_token,
                                        'owner_id': f'-{group_id}',
                                        'post_ids': post_ids,
                                        'v': '5.131'
                                    }).json()
        except Exception as e:
            print(f'error 2 {e} in {group_shortname}')

        try:
            sub_df_posts = pd.DataFrame(response['response'])
            df_posts = pd.concat([df_posts, sub_df_posts], ignore_index=True)
        except Exception as e:
            print(f'error 3 {e} with group {group_shortname}')
    try:
        merged_df = pd.merge(df_wall, df_posts, left_on='id', right_on='post_id')
        merged_df.drop('text', axis=1, inplace=True)
        merged_df.to_csv(f'assets_wall_posts_vk/{group_shortname}_wall_posts.csv', index=False)
    except Exception as e:
        print(f'error 4 {e} with group {group_shortname}')

    # try:
    #     engine = sqlalchemy.create_engine("mariadb+mariadbconnector://vk:yaro1997dobrg*M@173.249.18.74:3306/ads_reports")
    #     inspector = sqlalchemy.inspect(engine)
    #     table_name = f'{group_shortname}_wall_posts'
    #     if not inspector.has_table(table_name):
    #         merged_df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)
    #     merged_df.to_sql(table_name, engine, if_exists='replace', index=False)
    # except Exception as e:
    #     print(e)

    print(group_shortname)
