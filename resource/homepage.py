from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse


class HomePage(Resource):
    def get(self):
        return "InsFood Home Page"