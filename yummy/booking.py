# coding: utf-8

from flask_restful import Resource,  request
from flask import g
from . import db
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

user_ref = db.get_db().collection(u'users') or None
restaurants_ref = db.get_db().collection(u'restaurants') or None


class UserBooking(Resource):
    def get(self, user_name: str, booking_id: str):
        res = None
        if user_ref:
            res = user_ref.document(user_name).collection('bookings').document(booking_id).get()
            res = next(res)

        return res

    def post(self, user_name: str, booking_id: bool=None):
        booking = request.get_json(force=True)

        {'type': '', 'time': {'reserved': DatetimeWithNanoseconds(2019, 1, 27, 15, 30,
                                                                  tzinfo= < UTC >), 'booking': DatetimeWithNanoseconds(
            2019, 1, 27, 7, 22,
            tzinfo= < UTC >)}, 'no_of_customers': 2, 'restaurant': < google.cloud.firestore_v1beta1.document.DocumentReference
        object
        at
        0x7f217e3bebe0 >, 'location': < google.cloud.firestore_v1beta1._helpers.GeoPoint
        object
        at
        0x7f217e3d1588 >, 'no_of_tables': 1, 'booking_type': 'hotel'}]

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
