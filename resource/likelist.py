from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class CheckLikeList(Resource):
    
    def get(self, username):
        """ 
            user's like list
        """
        user_name = username.replace('%20', ' ')
        print("user_name: ", user_name)
        
        # check the user is in the database or not
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = '''
            SELECT r.name, r.categories, r.url, r.image_url, r.latitude, r.longitude, r.rating
            FROM Restaurant r JOIN (SELECT l.restaurant_id AS id
            FROM User u JOIN LikeList l ON u.user_id=l.user_id
            WHERE u.user_name = "{user_name}") As tmp ON r.restaurant_id=tmp.id 
        '''.format(user_name=user_name)
        print(sql)
        cursor.execute(sql)
        user_likelist = []
        for name in cursor:
            user_likelist.append(name)
        
        return user_likelist, 200
    
