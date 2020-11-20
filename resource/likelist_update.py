from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import mysql.connector
from mysql.connector import Error
from InsFood.database import db
from neo4j import GraphDatabase

class UpdateLikeList(Resource):
    
    # parser for post
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'user_name', type=str, required=True,
        help='{error_msg}'
    )
    post_parser.add_argument(
        'restaurant_name', type=str, required=True,
        help='{error_msg}'
    )
    '''
    post_parser.add_argument(
        'rating', type=int, required=True,
        help='{error_msg}'
    )
    '''
    '''
    # parser for delete
    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument(
        'user1_name', type=str, required=True,
        help='{error_msg}'
    )
    delete_parser.add_argument(
        'user2_name', type=str, required=True,
        help='{error_msg}'
    )
    '''
    
    def post(self):
        """ 
            user add a new restaurant to likelist
        """
        args = UpdateLikeList.post_parser.parse_args()
        user_name = args.get('user_name')
        restaurant_name = args.get('restaurant_name')
        #rating = args.get('rating')
        newlike = {
            'user_name':args.get('user_name'),
            'restaurant_name':args.get('restaurant_name')
            #'rating':args.get('rating')
        }
        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()

        # To get user's user_id
        user_id = []
        sql_1 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user_name)
        print(sql_1)
        cursor.execute(sql_1)
        for u in cursor:
            user_id.append(u)
        print(user_id) 

        # To get restaurant's restaurant_id
        restaurant_id = []
        sql_2 = 'SELECT restaurant_id FROM Restaurant WHERE name = "{restaurant_name}"'.format(restaurant_name=restaurant_name)
        print(sql_2)
        cursor.execute(sql_2)
        for u in cursor:
            restaurant_id.append(u)
        print(restaurant_id)

        # Insert new restaurant into LikeList table
        # neo4j may need insert data here
        uri = "bolt://localhost:7687"
        userName = "XDBoost"
        password = "xddd1234"
        graphDB_Driver = GraphDatabase.driver(uri, auth=(userName, password))
        cqlCreate = "MERGE (a:Person {id:"+str(user_id[0][0])+"}) MERGE (b:Restaurant {id:"+str(restaurant_id[0][0])+"}) MERGE (a)-[:Likes]->(b)"
        with graphDB_Driver.session() as graphDB_Session:
            graphDB_Session.run(cqlCreate)

        # user id is user_id[0][0], restaurant id is restaurant_id[0][0].
        sql_3 = "INSERT INTO LikeList (user_id, restaurant_id) VALUES ({user_id}, {restaurant_id});".format(user_id=user_id[0][0], restaurant_id=restaurant_id[0][0])
        print(sql_3)
        cursor.execute(sql_3)

        conn.commit()
        return newlike, 201
    
    def delete(self):
        """ 
            user remove liled restaurant from user's likelist
        """
        args = UpdateLikeList.post_parser.parse_args()
        user_name = args.get('user_name')
        restaurant_name = args.get('restaurant_name')

        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()

        # To get user's user_id
        user_id = []
        sql_1 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user_name)
        print(sql_1)
        cursor.execute(sql_1)
        for u in cursor:
            user_id.append(u)
        print(user_id) 

        # To get restaurant's restaurant_id
        restaurant_id = []
        sql_2 = 'SELECT restaurant_id FROM Restaurant WHERE name = "{restaurant_name}"'.format(restaurant_name=restaurant_name)
        print(sql_2)
        cursor.execute(sql_2)
        for u in cursor:
            restaurant_id.append(u)
        print(restaurant_id)

        # Delete liked restaurant from likelist table
        # neo4j may need delete data here
        uri = "bolt://localhost:7687"
        userName = "XDBoost"
        password = "xddd1234"
        graphDB_Driver = GraphDatabase.driver(uri, auth=(userName, password))
        cqlCreate = "MATCH (a:Person {id:"+str(user_id[0][0])+"})-[l:Likes]->(b:Restaurant {id:"+str(restaurant_id[0][0])+"}) DELETE l"
        with graphDB_Driver.session() as graphDB_Session:
            graphDB_Session.run(cqlCreate)

        # user id is user_id[0][0], restaurant id is restaurant_id[0][0].
        sql_3 = "DELETE FROM LikeList WHERE user_id={user_id} AND restaurant_id={restaurant_id};".format(user_id=user_id[0][0], restaurant_id=restaurant_id[0][0])
        print(sql_3)
        cursor.execute(sql_3)

        conn.commit()
        return 204
    