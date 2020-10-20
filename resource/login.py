from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str, required=True,
        help='{error_msg}'
    )
    parser.add_argument(
        'password', type=str, required=True,
        help='{error_msg}'
    )

    def post(self):
        """ 
            user login
        """
        
        args = Login.parser.parse_args()
        user_name = args.get('username')
        password  = args.get('password')
        print("user_name: ", user_name)
        print("password: ", password)
        # check the user is in the database or not
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = 'SELECT password FROM User WHERE user_name = "' + user_name + '"'
        # print(sql)
        cursor.execute(sql)
        passwd = []
        for p in cursor:
            passwd.append(p)
        print(passwd[0][0])
        if not passwd or passwd[0][0] != password:
            return 204
        
        return 200