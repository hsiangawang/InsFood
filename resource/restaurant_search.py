from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class RestaurantSearch(Resource):

    def get(self, restaurant):
        '''
            get information of specific restaurant
        '''
        restaurant_name = restaurant
        restaurant = []
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = 'SELECT name, categories, url, image_url, latitude, longitude, rating, phone, address, location, restaurant_id FROM Restaurant WHERE name = "' + restaurant_name + '"'
        cursor.execute(sql)

        for u in cursor:
            restaurant.append(u)

        return restaurant