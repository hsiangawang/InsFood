from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class UserUpdate(Resource):

    # parser for put
    put_parser = reqparse.RequestParser()
    put_parser.add_argument(
        'user_name', type=str, required=True,
        help='{error_msg}'
    )
    put_parser.add_argument(
        'nick_name', type=str, required=True,
        help='{error_msg}'
    )

    def put(self):
        '''
            update information of user
        '''
        args = UserUpdate.put_parser.parse_args()
        user_name = args.get('user_name')
        nick_name = args.get('nick_name')
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = 'UPDATE User SET nick_name = "{nick_name}" WHERE user_name = "{user_name}";'.format(user_name=user_name, nick_name=nick_name)
        cursor.execute(sql)

        conn.commit()
        return 204