from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db

class Logout(Resource):
    parser = reqparse.RequestParser()

    def post(self):
        """ 
            user logout
        """
        
        args = Logout.parser.parse_args()
        return {"message": "User log out!"}