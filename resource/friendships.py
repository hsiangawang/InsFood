from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class Friendships(Resource):
    def get(self):
        friendship_list = []
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        sql = "SELECT * FROM Friendship;"
        cursor.execute(sql)

        for u in cursor:
            friendship_list.append(u)

        return friendship_list