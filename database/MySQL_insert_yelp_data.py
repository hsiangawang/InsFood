# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 22:30:09 2020

@author: Jasmine Kuo
"""
import pandas as pd
import requests
import pymysql

api_key='wbc-PhiOmU5eP7jFV8pdfN-ZIYLONLk2x1_Wu7xdhjIX74nUfqp8VA8VfVjhRzmakv3d1cm3UyyOpGE-e2ntKJllZSqp8W8s3xvRakAoSgr7jCwr_nPMSyffxZB6X3Yx'
headers = {'Authorization': 'Bearer %s' % api_key}
url='https://api.yelp.com/v3/businesses/search'
data = []
for offset in range(0, 1000, 20):
    params = {
        'limit': 20, 
        'latitude': 40.116421,
        'longitude': -88.243385,
        'term': 'restaurants',
        'offset': offset
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data += response.json()['businesses']
    elif response.status_code == 400:
        print('400 Bad Request')
        break

need_data = [{key: data[i][key] for key in ['rating', 'name', 'categories', 'is_closed', 'url', 'image_url', 'coordinates']} for i in range(len(data))]
df = pd.DataFrame(need_data)
df = df[df['is_closed']==False]
df = df.drop('is_closed', axis = 1)
df = pd.concat([df, df['coordinates'].apply(pd.Series)], axis = 1).drop('coordinates', axis = 1)
df['categories'] = df['categories'].apply(lambda x: [x[i]['title'] for i in range(len(x))])
df['categories'] = df['categories'].apply(lambda x: str(','.join(x)))

# Connect to the database
conn = pymysql.connect(host='insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
                       port=3306,
                       user='admin', 
                       passwd='xddd1234',  
                       db='InsFood',
                       charset='utf8')

# Insert DataFrame recrds one by one.
sql = "INSERT INTO Restaurant(name, categories, url, image_url, latitude, longitude, rating) VALUES(%s,%s,%s,%s,%s,%s,%s)"

for i,row in df.iterrows():
    cursor=conn.cursor()
    cursor.execute(sql, tuple(row))
    # the connection is not autocommitted by default, so we must commit to save our changes
    conn.commit()
conn.close()




