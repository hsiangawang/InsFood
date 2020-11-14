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
for i in range(30):
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
friendship_df = pd.DataFrame([[a, b] for a in user_id for b in user_id if a != b], columns = ['user1_id', 'user2_id']).sample(100).reset_index(drop=True)

# Insert friendship data into MySQL database
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

# Connect to Neo4j DB
from neo4j import GraphDatabase

uri             = "bolt://localhost:7687"
userName        = "XDBoost"
password        = "xddd1234"

graphDB_Driver = GraphDatabase.driver(uri, auth=(userName, password))

# DELETE ALL DATA
cqlCreate = "MATCH (n) DETACH DELETE n"
with graphDB_Driver.session() as graphDB_Session:
    graphDB_Session.run(cqlCreate)

# Insert friendship data into Neo4j database
for i in range(friendship_df.shape[0]):
    user1_id = friendship_df['user1_id'][i]
    user2_id = friendship_df['user2_id'][i]
    cqlCreate = "MERGE (a:Person {id:"+str(user1_id)+"}) MERGE (b:Person {id:"+str(user2_id)+"}) MERGE (a)-[:Friends]->(b)"
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run(cqlCreate)

# Friendship sample code
'''
cqlCreate = "MERGE (a:Person {id:96}) MERGE (b:Person {id:62}) MERGE (a)-[:Friends]->(b)"
with graphDB_Driver.session() as graphDB_Session:
    graphDB_Session.run(cqlCreate)
'''    

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
likelist_df = pd.DataFrame([[a, b] for a in user_id for b in restaurant_id], columns = ['user_id', 'restaurant_id']).sample(300).reset_index(drop=True)

# Insert likelist data
conn = pymysql.connect(host='insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
                       port=3306,
                       user='admin', 
                       passwd='xddd1234',  
                       db='InsFood',
                       charset='utf8')

sql = "INSERT INTO LikeList(user_id, restaurant_id) VALUES(%s,%s)"

for i,row in likelist_df.iterrows():
    cursor=conn.cursor()
    cursor.execute(sql, tuple(row))
    # the connection is not autocommitted by default, so we must commit to save our changes
    conn.commit()
conn.close()

# Insert likelist data into Neo4j database
for i in range(likelist_df.shape[0]):
    restaurant_id = likelist_df['restaurant_id'][i]
    user_id = likelist_df['user_id'][i]
    cqlCreate = "MERGE (a:Person {id:"+str(user_id)+"}) MERGE (b:Restaurant {id:"+str(restaurant_id)+"}) MERGE (a)-[:Likes]->(b)"
    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run(cqlCreate)

# LikeList sample code
'''
cqlCreate = "MERGE (a:Person {id:96}) MERGE (b:Restaurant {id:1}) MERGE (a)-[:Likes]->(b)"
with graphDB_Driver.session() as graphDB_Session:
    graphDB_Session.run(cqlCreate)
'''


