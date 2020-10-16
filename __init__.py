from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from InsFood.resource.homepage import HomePage
from InsFood.resource.users import Users
from InsFood.resource.user_register import UserRegister

def create_app():

    app = Flask(__name__)
    api = Api(app)
    CORS(app) # This will enable CORS for all routes

    api.add_resource(HomePage, '/')
    api.add_resource(Users, '/users')
    api.add_resource(UserRegister, '/register')

    return app



