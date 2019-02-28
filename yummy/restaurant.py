# coding: utf-8

from flask_restful import Resource, reqparse, request
from .address import Address
from .location import Location
from .timing import Timing
from . import db
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('task')

restaurants_ref = db.get_db().collection(u'restaurants') or None


class Restaurant(Resource):

    def get(self, restaurant_name):
        res = None
        if restaurants_ref:
            # res = restaurants_ref.where(u'name', u'==', restaurant_name.lower()).get()
            # try:
            #     res = next(res)
            #     branchs = [branch.to_dict() for branch in res.reference.collection(u'branch').get()]
            #     for branch in branchs:
            #         branch['location'] = {'lat': branch['location'].latitude, 'lon': branch['location'].longitude}
            #     res = res.to_dict()
            #     res['branch'] = branchs
            # except StopIteration:
            #     res = None
            # res = restaurants_ref.document(restaurant_name).update({'name': 'new hotel'})
        return res.ListFields()[1:]

    def post(self, restaurant_name, area):

        arguments = request.get_json(force=True)
        arguments = restaurant_argument_parser(arguments)

        if restaurants_ref:
            # res = restaurants_ref.document(restaurant_name.lower()).collection('branch').document(area).get()
            # res = restaurants_ref.where(u'name', u'==', restaurant_name.lower()).get()
            # res = next(res)
            # res = res.reference.collection('branch').where('address.area', '==', area).get()
            # res = next(res)
            # res = restaurants_ref.document(restaurant_name.lower()).collection('branch').document(area).get()
            # time = res.update(arguments)

            res = restaurants_ref.document(restaurant_name).set({
                'name': restaurant_name,
                'rating': 0.0,
                'branch': {'abc': {
                    "location": {
                        "lat": 3.0,
                        "lon": 0.0
                    },
                    "address": {
                        "city": "",
                        "landmark": "",
                        "near_locality": "",
                        "country": "",
                        "area": ""
                    },
                    "table_max_capacity": 4,
                    "no_of_tables": 10,
                    "timing": {
                        "close": 22,
                        "open": 10
                    }
                }
                }
            })

        return


class Restaurants(Resource):

    def get(self):
        if restaurants_ref:
            restaurant_names = restaurants_ref.get()

            return {'restaurants':
                                [{'id': restaurant.id,
                                  'name': restaurant.get('name')}\
                                 for restaurant in restaurant_names]}

        return {'restaurants': ''}


def restaurant_argument_parser(args):
    assert type(args) is type(dict())

    delete_keys = []
    new_args = {}
    for key, value in args.items():
        if isinstance(value, dict):
            delete_keys.append(key)
            for k, v in value.items():
                new_args[key+'.'+k] = v
    for key in delete_keys:
        args.pop(key, None)

    args.update(new_args)
    return args


class RestaurantDetails:

    def __init__(self, name: str, rating: float):
        self.name = name.lower().title()
        self.rating = float(rating)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, restaurant):
        return cls(**restaurant)

class RestaurantBranch:

    def __init__(self, address: Address, location: Location, timing: Timing,
                 no_of_tables: int, table_max_capacity: int):
        self.address = address
        self.location = location
        self.timing = timing
        self.no_of_tables = no_of_tables
        self.table_max_capacity = table_max_capacity
