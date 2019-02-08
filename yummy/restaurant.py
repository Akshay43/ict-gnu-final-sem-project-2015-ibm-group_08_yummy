# coding: utf-8

from flask_restful import Resource, reqparse
import global_constants
from address import Address
from location import Location
from timing import Timing


parser = reqparse.RequestParser()
parser.add_argument('task')

restaurants_ref = global_constants.DB.collection(u'restaurants') or None

class Restaurant(Resource):

    def get(self, restaurant_name):
        res = None
        if restaurants_ref:
            #restaurants_ref.where(u'name', u'==', restaurant_name.title()).get()
            res = restaurants_ref.document(restaurant_name.lower()).get()
        return res

    def post(self, name):
        args = parser.parse_args()

        if restaurants_ref:
            # restaurants.set()
            pass
        return args


class Restaurants(Resource):

    def get(self):
        if restaurants_ref:
            restaurant_names = restaurants_ref.get()
            return {name['name'] for name in restaurant_names}

        return {}


class RestaurantDetails:

    def __init__(self, name: str, rating: float):
        self.name = name.lower().title()
        self.rating = float(rating)

    def to_dict(self):
        return self.__dict__

    def from_dict(self, restaurant):
        self.name = restaurant.get('name', None)
        self.rating = restaurant.get('rating', None)

class RestaurantBranch:

    def __init__(self, address: Address, location: Location, timing: Timing,
                 no_of_tables: int, table_max_capacity: int):
        self.address = address
        self.location = location
        self.timing = timing
        self.no_of_tables = no_of_tables
        self.table_max_capacity = table_max_capacity
