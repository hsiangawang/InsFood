from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class Restaurants(Resource):
    def get(self):
        restaurant_list = []
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = "SELECT * FROM Restaurant;"
        cursor.execute(sql)

        for u in cursor:
            restaurant_list.append(u)

        return restaurant_list