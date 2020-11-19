from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from InsFood.resource.homepage import HomePage
from InsFood.resource.users import Users
from InsFood.resource.user import UserInfo
from InsFood.resource.user_update import UserUpdate
from InsFood.resource.user_register import UserRegister
from InsFood.resource.login import Login
from InsFood.resource.logout import Logout
from InsFood.resource.restaurants import Restaurants
from InsFood.resource.restaurant_search import RestaurantSearch
from InsFood.resource.friendships import Friendships
from InsFood.resource.friendship import CheckFriends
from InsFood.resource.friendship_update import UpdateFriends
from InsFood.resource.likelists import Likelists
from InsFood.resource.likelist import CheckLikeList
from InsFood.resource.likelist_update import UpdateLikeList
from InsFood.resource.tag_recommend import tagRecommend

def create_app():

    app = Flask(__name__)
    api = Api(app)
    CORS(app) # This will enable CORS for all routes

    api.add_resource(HomePage, '/')
    api.add_resource(Users, '/users') # testing route
    api.add_resource(UserUpdate, '/user')
    api.add_resource(UserInfo, '/user/<string:username>')
    api.add_resource(UserRegister, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(Restaurants, '/restaurants')
    api.add_resource(RestaurantSearch, '/search/<string:restaurant>')
    api.add_resource(Friendships, '/friendships') # testing route
    api.add_resource(CheckFriends, '/friendship/<string:username>')
    api.add_resource(UpdateFriends, '/friendship')
    api.add_resource(Likelists, '/likelists') # testing route
    api.add_resource(CheckLikeList, '/likelist/<string:username>')
    api.add_resource(UpdateLikeList, '/likelist')
    api.add_resource(tagRecommend, '/tagRecommend/<string:user_name>/<string:friend_name>')

    return app



