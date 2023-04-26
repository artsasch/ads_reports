import pandas as pd
import json


with open('response.json', 'r') as infile:
    data = json.load(infile)

df = pd.json_normalize(data['response'])

df = df.drop(['reach.age',
              'reach.cities',
              'reach.countries',
              'reach.sex',
              'reach.sex_age',
              'visitors.age',
              'visitors.cities',
              'visitors.countries',
              'visitors.mobile_views',
              'visitors.sex',
              'visitors.sex_age'
              ], axis=1)


df.loc[:, ['period_from', 'period_to']] = df.loc[:, ['period_from', 'period_to']].apply(pd.to_datetime, unit='s')
df[['period_from', 'period_to']] = df[['period_from', 'period_to']].apply(lambda x: x.dt.strftime('%m/%d/%Y'))


df.to_csv('test_data.csv', index=False)
