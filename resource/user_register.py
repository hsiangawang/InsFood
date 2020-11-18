from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str, required=True,
        help='{error_msg}'
    )
    parser.add_argument(
        'nickname', type=str, required=True,
        help='{error_msg}'
    )
    parser.add_argument(
        'password', type=str, required=True,
        help='{error_msg}'
    )

    def post(self):
        """ 
            register a new user
        """
        args = UserRegister.parser.parse_args()
        user_name = args.get('username')
        password  = args.get('password')
        nick_name = args.get('nickname')
        user = {
            'username':args.get('username'),
            'nickname':args.get('nickname'),
            'password':args.get('password')
        }
        # neo4j may need to add user here
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = "INSERT INTO User (user_name, password, nick_name) VALUES (%s, %s, %s);"
        new_data = (user_name, password, nick_name)
        cursor.execute(sql, new_data)

        conn.commit()
        return user, 201