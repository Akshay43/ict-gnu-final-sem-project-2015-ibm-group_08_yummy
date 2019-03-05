from flask import Flask, g
from flask_restful import Api
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # CREDENTIALS = os.path.abspath(os.listdir(os.path.join(app.instance_path, 'credentials'))),
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


app = create_app()

api = Api(app)
with app.app_context():
    from .booking import UserBooking, UserBookings, RestaurantBooking, RestaurantBookings
    from .restaurants import Restaurant, Restaurants
    from .users import User, Users

api.add_resource(User, '/user/<string:user_name>')
api.add_resource(Users, '/users')
api.add_resource(Restaurant, '/<string:restaurant_name>',
                 '/<string:restaurant_name>/<string:area>', endpoint='restaurant')
api.add_resource(Restaurants, '/restaurants')
api.add_resource(UserBooking, '/user/<string:user_name>/booking/<string:booking_id>')
api.add_resource(RestaurantBooking,
                 '/restaurant/<string:restaurant_name>/booking/<string:booking_id>')

api.add_resource(RestaurantBookings, '/restaurant/<string:restaurant_name>/bookings')
api.add_resource(UserBookings, '/user/<string:user_name>/bookings/')

if __name__ == '__main__':
    app.run(debug=True)
