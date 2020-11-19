from flask_restful import Resource, Api, reqparse
from neo4j import GraphDatabase
from InsFood.database import db
from collections import Counter

class friendzoneRecommend(Resource):
    def get(self, user_name):
        """
        give user recommendation from friend zone
        """
        user_name = user_name.replace('%20', ' ')
        print("user_name: ", user_name)

        conn = db.create_connection(db.connection_config_dict)
        cursor = conn.cursor()
        # To get user's user_id
        user_id_list = []
        sql_1 = 'SELECT user_id FROM User WHERE user_name = "{user_name}"'.format(user_name=user_name)
        print(sql_1)
        cursor.execute(sql_1)
        for u in cursor:
            user_id_list.append(u)
        print(user_id_list)
        user_id = user_id_list[0][0]

        uri = "bolt://localhost:7687"
        userName = "XDBoost"
        password = "xddd1234"
        graphDB_Driver = GraphDatabase.driver(uri, auth=(userName, password))

        cqlQuery1 = "MATCH (a:Person {id:{user_id}}})-[:Friends]->(b:Person)-[:Likes]->(r:Restaurant) RETURN r.id".format(user_id = user_id)
        cqlQuery2 = "MATCH (a:Person {id:{user_id}})-[:Friends]->(b:Person)-[:Friends]->(c:Person)-[:Likes]->(r:Restaurant) WHERE a.id <> c.id RETURN r.id".format(user_id = user_id)
        with graphDB_Driver.session() as graphDB_Session:
            r1 = graphDB_Session.run(cqlQuery1)
            r2 = graphDB_Session.run(cqlQuery2)

        r1_list = [item for elem in [r.values() for r in r1] for item in elem]
        r2_list = [item for elem in [r.values() for r in r2] for item in elem]

        recomm_restaurants_id = [i[0] for i in Counter(r1_list + r2_list).most_common(5)]

        sql_2 = "SELECT name, url, image_url FROM InsFood.Restaurant WHERE restaurant_id IN {recomm_restaurants}".format(recomm_restaurants = tuple(recomm_restaurants_id))
        cursor.execute(sql_2)
        recomm_restaurants_list = []
        for restaurant in cursor:
            recomm_restaurants_list.append(restaurant)

        conn.close()

        if not recomm_restaurants_list:
            return ['fail']
        else:
            return recomm_restaurants_list, 200
