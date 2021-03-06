from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class UpdateFriends(Resource):

    # parser for post
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'user1_name', type=str, required=True,
        help='{error_msg}'
    )
    post_parser.add_argument(
        'user2_name', type=str, required=True,
        help='{error_msg}'
    )
    # parser for delete
    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument(
        'user1_name', type=str, required=True,
        help='{error_msg}'
    )
    delete_parser.add_argument(
        'user2_name', type=str, required=True,
        help='{error_msg}'
    )

    def post(self):
        """ 
            user make a new friend
        """
        args = UpdateFriends.post_parser.parse_args()
        user1_name = args.get('user1_name')
        user2_name = args.get('user2_name')
        friendship = {
            'user1_name':args.get('user1_name'),
            'user2_name':args.get('user2_name')
        }
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()

        # To get user1's user_id
        user1_id = []
        sql_1 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user1_name)
        print(sql_1)
        cursor.execute(sql_1)
        for u in cursor:
            user1_id.append(u)
        print(user1_id) 

        # To get user2's user_id
        user2_id = []
        sql_2 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user2_name)
        print(sql_2)
        cursor.execute(sql_2)
        for u in cursor:
            user2_id.append(u)
        print(user2_id)

        # Insert new friendship into friendship table
        # neo4j may need insert data here
        # user1 id is user1_id[0][0], user2 id is user2_id[0][0].
        sql_3 = "INSERT INTO Friendship (user1_id, user2_id) VALUES ({user1_id}, {user2_id});".format(user1_id=user1_id[0][0], user2_id=user2_id[0][0])
        print(sql_3)
        cursor.execute(sql_3)

        conn.commit()
        return friendship, 201

    def delete(self):
        """ 
            user remove friendship with another user
        """
        args = UpdateFriends.post_parser.parse_args()
        user1_name = args.get('user1_name')
        user2_name = args.get('user2_name')

        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()

        # To get user1's user_id
        user1_id = []
        sql_1 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user1_name)
        print(sql_1)
        cursor.execute(sql_1)
        for u in cursor:
            user1_id.append(u)
        print(user1_id) 

        # To get user2's user_id
        user2_id = []
        sql_2 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user2_name)
        print(sql_2)
        cursor.execute(sql_2)
        for u in cursor:
            user2_id.append(u)
        print(user2_id)

        # Delete friendship from friendship table
        # neo4j may need delete data here
        # user1 id is user1_id[0][0], user2 id is user2_id[0][0].
        sql_3 = "DELETE FROM Friendship WHERE user1_id={user1_id} AND user2_id={user2_id};".format(user1_id=user1_id[0][0], user2_id=user2_id[0][0])
        print(sql_3)
        cursor.execute(sql_3)

        conn.commit()
        return 204