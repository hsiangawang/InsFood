from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db
from collections import defaultdict

class tagRecommend(Resource):
    
    def get(self, user_id, friend_id):
        """ 
            give user recommendation from common liked tag of restaurant from friend
        """
        print("user_id: ", user_id)
        print("friend_id: ", friend_id)
        
        # 
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
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
    
