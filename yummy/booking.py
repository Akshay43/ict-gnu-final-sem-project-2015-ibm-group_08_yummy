# coding: utf-8

from flask_restful import Resource,  request

class Booking(Resource):

    def get(self, user_name, booking_id):
        return request.full_path


class Bookings(Resource):

    def get(self, name):
        """name: username | restaurant_name"""
        return name