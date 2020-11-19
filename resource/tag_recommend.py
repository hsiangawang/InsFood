from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db
from collections import defaultdict

class tagRecommend(Resource):
    
    def get(self, user_name, friend_name):
        """ 
            give user recommendation from common liked tag of restaurant from friend
        """
        user_name = user_name.replace('%20', ' ')
        friend_name = friend_name.replace('%20', ' ')
        print("user_name: ", user_name)
        print("friend_name: ", friend_name)

        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        # To get user's user_id
        user_id_list = []
        sql_1 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user_name)
        print(sql_1)
        cursor.execute(sql_1)
        for u in cursor:
            user_id_list.append(u)
        print(user_id_list)
        user_id = user_id_list[0][0] 

        # To get friend's user_id
        friend_id_list = []
        sql_2 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=friend_name)
        print(sql_2)
        cursor.execute(sql_2)
        for u in cursor:
            friend_id_list.append(u)
        print(friend_id_list)
        friend_id = friend_id_list[0][0] 
        
        # 
        sql_findTag = '''
            SELECT r.name, r.url, r.image_url, r.categories
            FROM   Restaurant r JOIN LikeList l ON r.restaurant_id = l.restaurant_id
            WHERE  l.user_id = {user_id}
        '''.format(user_id=user_id)
        print(sql_findTag)
        cursor.execute(sql_findTag)
        liked_restaurants = []
        for restaurant in cursor:
            liked_restaurants.append(restaurant)
        print("liked_restaurants: ", liked_restaurants)

        # Create a dictionary to record the apperance times of each tag
        tag_times = defaultdict(int)
        for r in liked_restaurants:
            categories = r[3]
            tags = categories.split(',')
            for tag in tags:
                tag_times[tag] += 1
        print("tag_times: ", tag_times)

        cnt = sorted(tag_times.items(), key = lambda x : x[1], reverse=True)
        print("most tag: ", cnt[0][0])
        most_tag = str(cnt[0][0])
        # get recommended restaurants
        sp_sql = 'CALL getTagRecommend({friend_id}, "{tag}");'.format(friend_id=friend_id, tag=most_tag)
        print("sp_sql: ", sp_sql)
        cursor.execute(sp_sql)
        tag_recommend_restaurant = []
        for res in cursor:
            tag_recommend_restaurant.append(res)

        # if no common tag, return of of restaurant liked by friend
        if not tag_recommend_restaurant:
            tmp = liked_restaurants[0]
            tmp_res = (tmp[0], tmp[1],tmp[2])
            tag_recommend_restaurant.append(tmp_res)

        return tag_recommend_restaurant,200
    
