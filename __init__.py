from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from InsFood.resource.homepage import HomePage
from InsFood.resource.users import Users
from InsFood.resource.user_register import UserRegister
from InsFood.resource.login import Login
from InsFood.resource.logout import Logout
from InsFood.resource.restaurants import Restaurants
from InsFood.resource.restaurant_search import RestaurantSearch

def create_app():

    app = Flask(__name__)
    api = Api(app)
    CORS(app) # This will enable CORS for all routes

    api.add_resource(HomePage, '/')
    api.add_resource(Users, '/users') # testing route
    api.add_resource(UserRegister, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(Restaurants, '/restaurants')
    api.add_resource(RestaurantSearch, '/search')

    return app



