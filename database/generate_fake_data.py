# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 22:43:09 2020

@author: Jasmine Kuo
"""
import pandas as pd
import numpy as np
import requests
import pymysql
import names

#==================#
#====== User ======#
#==================#

# Generate user data
user_list = []
for i in range(100):
    tmp = names.get_full_name()
    user_list.append([tmp, tmp.replace(" ", "")[::-1], tmp.split(' ')[0]])
user_df = pd.DataFrame(user_list, columns = ['user_name', 'password', 'nick_name'])


conn = pymysql.connect(host='insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
                       port=3306,
                       user='admin', 
                       passwd='xddd1234',  
                       db='InsFood',
                       charset='utf8')

# Insert user data
sql = "INSERT INTO User(user_name, password, nick_name) VALUES(%s,%s,%s)"

for i,row in user_df.iterrows():
    cursor=conn.cursor()
    cursor.execute(sql, tuple(row))
    # the connection is not autocommitted by default, so we must commit to save our changes
    conn.commit()
conn.close()

#========================#
#====== Friendship ======#
#========================#
# Get user_id from User table
conn = pymysql.connect(host='insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
                       port=3306,
                       user='admin', 
                       passwd='xddd1234',  
                       db='InsFood',
                       charset='utf8')

sql = "SELECT user_id FROM InsFood.User"
cursor = conn.cursor()
cursor.execute(sql)
records = cursor.fetchall()
user_id = [element for tupl in records for element in tupl]
conn.close()

# Pair user_id for friendship
import random 
import itertools 
def get_random_pairs(numbers): 
  # Generate all possible non-repeating pairs 
  pairs = list(itertools.combinations(numbers, 2)) 
 
  # Randomly shuffle these pairs 
  random.shuffle(pairs) 
  return pairs

friendship_df = pd.DataFrame(get_random_pairs(user_id), columns = ['user1_id', 'user2_id']).sample(100)

# Insert friendship data
conn = pymysql.connect(host='insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
                       port=3306,
                       user='admin', 
                       passwd='xddd1234',  
                       db='InsFood',
                       charset='utf8')

sql = "INSERT INTO Friendship(user1_id, user2_id) VALUES(%s,%s)"

for i,row in friendship_df.iterrows():
    cursor=conn.cursor()
    cursor.execute(sql, tuple(row))
    # the connection is not autocommitted by default, so we must commit to save our changes
    conn.commit()
conn.close()

#======================#
#====== LikeList ======#
#======================#
# Get restaurant_id from Restaurant table
conn = pymysql.connect(host='insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
                       port=3306,
                       user='admin', 
                       passwd='xddd1234',  
                       db='InsFood',
                       charset='utf8')

sql = "SELECT restaurant_id FROM InsFood.Restaurant"
cursor = conn.cursor()
cursor.execute(sql)
records = cursor.fetchall()
restaurant_id = [element for tupl in records for element in tupl]
conn.close()

# Pair restaurant_id and user_id
likelist_df = pd.DataFrame([[a, b] for a in user_id for b in restaurant_id], columns = ['user_id', 'restaurant_id']).sample(100)
likelist_df['rating'] = np.random.uniform(low=1, high=5, size=(100,)).astype(int)

# Insert likelist data
conn = pymysql.connect(host='insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
                       port=3306,
                       user='admin', 
                       passwd='xddd1234',  
                       db='InsFood',
                       charset='utf8')

# Insert DataFrame recrds one by one.
sql = "INSERT INTO LikeList(user_id, restaurant_id, rating) VALUES(%s,%s,%s)"

for i,row in likelist_df.iterrows():
    cursor=conn.cursor()
    cursor.execute(sql, tuple(row))
    # the connection is not autocommitted by default, so we must commit to save our changes
    conn.commit()
conn.close()

