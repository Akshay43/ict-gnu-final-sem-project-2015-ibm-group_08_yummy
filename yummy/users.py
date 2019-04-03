# coding: utf-8
from flask_restful import Resource
from flask import g, request, abort
from . import _util

# todo: change below constant with file name
user_ref = g.db.collection(u'users') or None


class User(Resource):
    username_service = _util.registered_usernames()

    def get(self, user_name: str):
        res = None
        if user_ref:
            res = user_ref.document(user_name).get()
            res = res.to_dict()
            # todo: make DatetimeWithNanoSeconds, GeoPoint Json Serializable
            res.pop('last_login')
            res.pop('token_timestamp')
            res.pop('location')
            print(res)
        return res

    def post(self, user_name: str):
        res = None

        # TODO: verify user using User class
        user = request.get_json(force=True)
        if user_name != user['username']:
            return abort(400)

        if User.username_service.username_exsist(user_name):
            return abort(400, 'username already exsist')
        # Here user won't have any booking
        # todo: create user with booking
        if user_ref:
            try:
                user_ref.document(user_name).set(user)
                res = True
                User.username_service.insert_username(user_name)
            except:
                return res, 400
        return res

    def put(self, user_name):
        print('put is called')
        res = None
        print(request.__dict__['data'])
        user = request.get_json()

        if user_ref:
            user = _util.parse_args_for_update(user)
        #     # try:
            user_ref.document(user_name).update(user)
            res = True
            # except:
            #     return res, 400
        return res


class Users(Resource):

    def get(self):
        res = None
        if user_ref:
            users = user_ref.get()
            res = [{'id': user.id,
                    'username': user.get('name')}for user in users]
        return res
