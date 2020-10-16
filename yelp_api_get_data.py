# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 22:30:09 2020

@author: Jasmine Kuo
"""

import requests

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

need_data = [{key: data[i][key] for key in ['id', 'name', 'categories', 'is_closed', 'url', 'image_url', 'coordinates']} for i in range(len(data))]

placeholders = ', '.join(['%s'] * len(dict_data))
columns = ', '.join(dict_data.keys())
sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
cursor.execute(sql, dict_data.values())

