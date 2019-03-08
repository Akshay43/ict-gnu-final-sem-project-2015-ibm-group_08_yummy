# coding: utf-8

from flask_restful import Resource, request, abort
from flask import g
from . import db
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from . import _util
from datetime import datetime

user_ref = db.get_db().collection(u'users') or None
restaurants_ref = db.get_db().collection(u'restaurants') or None


class UserBooking(Resource):
    def get(self, user_name: str, booking_id: str =None):
        booking_req = request.get_json(force=True)
        print(booking_req)
        return user_name
        res = None
        if user_ref:
            res = user_ref.document(user_name).collection('bookings').document(booking_id).get()
            res = next(res)

        return res

    """
    {
        "restaurant_name": "neelkant",
        "restaurant_area": "rakhial",
        "user_id": "kalpit",
        "type": "",
        "location":{"latitude": 1.0, "longitude":1.0},
        "time": {"year": 2019, "month": 3, "day": 8, "hour":12, "minute":30},
        "no_of_tables": 1,
        "no_of_customer": 1,
        "booking_type": "hotel"
    }
    """
    def post(self, user_name: str):
        print("hello")
        booking_req = request.get_json(force=True)
        print(booking_req)
        user_id = booking_req.pop('user_id', None)
        res = None
        if not user_id:
            abort(400)

        if user_ref and restaurants_ref:
            user_booking = RegisterUserBooking.from_dict(booking_req.copy())

            booking_res = user_ref.document(user_name).collection('bookings').add(user_booking.to_dict())

            if booking_res:
                restaurant_name = booking_req.pop('restaurant_name', None)
                restaurant_area = booking_req.pop('restaurant_area', None)
                booking_req['user'] = user_id
                register_user_booking_restaurant = RegisterRestaurantBooking.from_dict(booking_req)
                if restaurant_name and restaurant_area:

                    restaurants_ref.document(restaurant_name).collection('branch')\
                        .document(restaurant_area).collection('bookings').add(register_user_booking_restaurant.to_dict())
                else:
                    #revert_user_changes
                    pass
            else:
                abort(400)

        else:
            abort(400)
        return True



class UserBookings(Resource):

    def get(self, user_name):
        res = None
        print('userbooking get')
        if user_ref:
            res = user_ref.document(user_name).collection('bookings').get()
            res = [booking.to_dict() for booking in res]
            print(res)
        return res


class RestaurantBooking(Resource):
    pass


class RestaurantBookings(Resource):

    def get(self, user_name, booking_id):
        return request.full_path


class BookingTime():
    """TODO: Add all timing operation from datetime module"""

    def __init__(self, year, month, day, hour, minute):
        self.booking = DatetimeWithNanoseconds.from_rfc3339(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.reserved = DatetimeWithNanoseconds(year=year, month=month, day=day, hour=hour, minute=minute)

    def __str__(self):
        """ TODO: update str"""
        return self.__dict__

    @classmethod
    def from_dict(cls, timing):
        return cls(**timing)


class RegisterUserBooking:
    _fields = {
        'location': _util.geopoint_from_dict,
    }

    def __init__(self, type: str, location, restaurant, time: BookingTime,
                 no_of_tables: int, no_of_customer: int, booking_type: str):
        self.type = type
        self.location = location
        self.time = time
        self.no_of_tables = no_of_tables
        self.no_of_customer = no_of_customer
        self.booking_type = booking_type
        self.restaurant = restaurant

    @classmethod
    def from_dict(cls, restaurant):
        print(restaurant)
        args = {}
        for key, value in RegisterUserBooking._fields.items():
            try:
                args[key] = value(restaurant[key])
                restaurant.pop(key)
                # args[key] = RegisterUserBooking._fields[key](**value)
            except (TypeError):
                print('error')

        restaurant_name = restaurant.pop('restaurant_name', None)
        restaurant_area = restaurant.pop('restaurant_area', None)

        if restaurant_name and restaurant_area:
            args['restaurant'] = restaurants_ref.document(restaurant_name).collection('branch')\
                                                .document(restaurant_area)
        args['time'] = {
            'reserved': _util.convert_to_date_from_dict(restaurant.pop('time')),
            'booking': _util.get_current_date()
        }

        args.update(restaurant)
        print(args)
        return cls(**args)

    def to_dict(self):
        return self.__dict__


class RegisterRestaurantBooking:
    _fields = {

        'location': _util.geopoint_from_dict,
        'user': user_ref.document,

    }

    def __init__(self, type, location, user, time: BookingTime,
                 no_of_tables: int, no_of_customer: int, booking_type: str):
        self.type = type
        self.location = location
        self.time = time
        self.no_of_tables = no_of_tables
        self.no_of_customer = no_of_customer
        self.booking_type = booking_type
        self.user = user

    @classmethod
    def from_dict(cls, user):
        print('user', user)
        args = {}
        for key, value in RegisterRestaurantBooking._fields.items():
            try:
                args[key] = value(user.pop(key))
                # args[key] = RegisterRestaurantBooking._fields[key](**value)
            except TypeError:
                pass

        args['time'] = {
            'reserved': _util.convert_to_date_from_dict(user.pop('time')),
            'booking': _util.get_current_date()
        }

        # args['user'] = user_ref.document(user.pop('user_id'))

        args.update(user)

        return cls(**args)

    def to_dict(self):
        return self.__dict__
