from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class CheckFriends(Resource):

    def get(self, username):
        """ 
            user's friends
        """
        user_name = username.replace('%20', ' ')
        print("user_name: ", user_name)
        
        # check the user is in the database or not
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = '''
            SELECT u.user_name
            FROM User u JOIN (SELECT fr.user2_id AS id
            FROM User u JOIN Friendship fr ON u.user_id=fr.user1_id
            WHERE u.user_name = "{user_name}") As tmp ON u.user_id=tmp.id 
        '''.format(user_name=user_name)
        print(sql)
        cursor.execute(sql)
        user_friend = []
        for name in cursor:
            user_friend.append(name)
        
        return user_friend, 200