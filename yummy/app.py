from flask import Flask, g
from flask_restful import Api
from db import init_db


def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app


app = create_app()
api = Api(app)

from booking import Booking, Bookings
from restaurant import Restaurant, Restaurants
from user import User, Users
import global_constants

api.add_resource(User, '/user/<string:user_name>')
api.add_resource(Users, '/users')
api.add_resource(Restaurant, '/restaurant/<string:restaurant_name>')
api.add_resource(Restaurants, '/restaurants')
api.add_resource(Booking, '/user/<string:user_name>/booking/<string:booking_id>',
                            '/restaurant/<string:restaurant_name>/booking/<string:booking_id>')
api.add_resource(Bookings, '/restaurant/<string:name>/bookings',
                            '/user/<string:name>/bookings/')

if __name__ == '__main__':
    app.run(debug=True)
