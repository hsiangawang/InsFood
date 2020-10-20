from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class RestaurantSearch(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'restaurant_name', type=str, required=True,
        help='{error_msg}'
    )
    

    def get(self):
        '''
            get information of specific restaurant
        '''
        args = RestaurantSearch.parser.parse_args()
        restaurant_name = args.get('restaurant_name')
        restaurant = []
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = 'SELECT name, categories, url, image_url, latitude, longtitude FROM Restaurant WHERE name = "' + restaurant_name + '"'
        cursor.execute(sql)

        for u in cursor:
            restaurant.append(u)

        return restaurant