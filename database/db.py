# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:06:27 2020

@author: Jasmine Kuo
"""
# pip install mysql-connector-python
import mysql.connector
from mysql.connector import Error

connection_config_dict = {
    'user': 'admin',
    'password': 'xddd1234',
    'host': 'insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com',
    'database': 'InsFood'
}

def create_connection(db_info):
    try:
        connection = mysql.connector.connect(**db_info)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)

def create_table(conn, create_table_sql, table_name):
    try:
        cursor = conn.cursor()
        result = cursor.execute(create_table_sql)
        print(table_name + "Table created successfully")
    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if conn.is_connected():
            cursor.close()
            print("MySQL connection is closed")

def drop_table_if_exists(conn, drop_table_sql):
    try:
        cursor = conn.cursor()
        result = cursor.execute(drop_table_sql)
        print("Drop table if exists")
    except mysql.connector.Error as error:
        print("Failed to drop table in MySQL: {}".format(error))
    finally:
        if conn.is_connected():
            cursor.close()
            print("MySQL connection is closed")

def create_stored_procedure(conn, stored_procedure_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(stored_procedure_sql)
        print("Create stored procedure")
    except mysql.connector.Error as error:
        print("Failed to create procedure in MySQL: {}".format(error))
    finally:
        print("!")
        if conn.is_connected():
            cursor.close()
            print("MySQL connection is closed")

def drop_sp_if_exists(conn, drop_sp_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(drop_sp_sql)
        print("Drop sp if exists")
    except mysql.connector.Error as error:
        print("Failed to drop sp in MySQL: {}".format(error))
    finally:
        if conn.is_connected():
            cursor.close()
            print("MySQL connection is closed")

def main():
    
    conn = create_connection(connection_config_dict)
    
    user_table_create = """CREATE TABLE IF NOT EXISTS User ( 
                         user_id int(20) AUTO_INCREMENT NOT NULL,
                         user_name varchar(128) NOT NULL,
                         password varchar(128) NOT NULL,
                         nick_name varchar(128) NOT NULL,
                         PRIMARY KEY (user_id)); """
    
    
    friendship_table_create = """CREATE TABLE IF NOT EXISTS Friendship ( 
                         friendship_id int(20) AUTO_INCREMENT NOT NULL,
                         user1_id int(20) NOT NULL,
                         user2_id int(20) NOT NULL,
                         PRIMARY KEY (friendship_id),
                         FOREIGN KEY (user1_id)
                             REFERENCES User(user_id)
                             ON DELETE CASCADE
                             ON UPDATE CASCADE); """
    
    
    restaurant_table_create = """CREATE TABLE IF NOT EXISTS Restaurant ( 
                         restaurant_id int(20) AUTO_INCREMENT NOT NULL,
                         name varchar(128) NOT NULL,
                         review_count int(20) NOT NULL,
                         categories varchar(128) NOT NULL,
                         url varchar(128) NOT NULL,
                         image_url varchar(128) NOT NULL,
                         latitude varchar(45) NOT NULL,
                         longitude varchar(45) NOT NULL,
                         rating real NOT NULL,
                         phone varchar(45) NOT NULL,
                         address varchar(128) NOT NULL,
                         location varchar(128) NOT NULL,
                         PRIMARY KEY (restaurant_id)); """
    
    like_table_create = """CREATE TABLE IF NOT EXISTS LikeList ( 
                         user_restaurant_id int(20) AUTO_INCREMENT NOT NULL,
                         restaurant_id int(20),
                         user_id int(20) NOT NULL,
                         PRIMARY KEY (user_restaurant_id),
                         FOREIGN KEY (user_id)
                             REFERENCES User(user_id)
                             ON DELETE CASCADE
                             ON UPDATE CASCADE,
                         FOREIGN KEY (restaurant_id)
                             REFERENCES Restaurant(restaurant_id)
                             ON DELETE SET NULL
                             ON UPDATE CASCADE); """
    
    # initialize db
    user_table_drop = """DROP TABLE IF EXISTS User"""
    friendship_table_drop = """DROP TABLE IF EXISTS Friendship"""
    restaurant_table_drop = """DROP TABLE IF EXISTS Restaurant"""
    likelist_table_drop = """DROP TABLE IF EXISTS LikeList"""

    # drop sp if exists
    drop_tag_sp = """DROP PROCEDURE IF EXISTS getTagRecommend;"""

    # create stored procedure
    tag_stored_procedure = '''
    CREATE PROCEDURE getTagRecommend(IN friend_id integer, IN tag varchar(30))
    BEGIN
        SELECT r.name, r.url, r.image_url
        FROM   Restaurant r JOIN LikeList l ON r.restaurant_id = l.restaurant_id
        WHERE  l.user_id = friend_id AND r.categories LIKE CONCAT('%', tag, '%');

    END

    DELIMITER ;
    '''

    if conn is not None:
        drop_table_if_exists(conn, likelist_table_drop)
        drop_table_if_exists(conn, friendship_table_drop)
        drop_table_if_exists(conn, restaurant_table_drop)
        drop_table_if_exists(conn, user_table_drop)
        create_table(conn, user_table_create, 'User')
        create_table(conn, friendship_table_create, 'Friendship')
        create_table(conn, restaurant_table_create, 'Restaurant')
        create_table(conn, like_table_create, 'LikeList')
        #drop_sp_if_exists(conn, drop_tag_sp)
        #create_stored_procedure(conn, tag_stored_procedure)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()


