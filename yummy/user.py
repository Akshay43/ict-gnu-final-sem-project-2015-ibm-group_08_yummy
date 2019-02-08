# coding: utf-8
from flask_restful import Resource


class User(Resource):

    def get(self, name='anil'):
        return 'Hello ' + name


class Users(Resource):

    def get(self):
        return 'users'
