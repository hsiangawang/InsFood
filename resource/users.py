from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class Users(Resource):
    def get(self):
        user_list = []
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = "SELECT * FROM User;"
        cursor.execute(sql)

        for u in cursor:
            user_list.append(u)

        return user_list