from google.cloud import firestore
from .user_exception import DBNotInitialized, CredentialsNotFound
import os
from flask import g
import click
from flask.cli import with_appcontext

credentials = os.path.split(os.path.realpath(__file__))[0]
credentials = os.path.join(credentials, 'credentials', 'yummy-g08-807d7ab294cf.json')
print(credentials)


def init_db():
    if not os.path.exists(credentials):
        raise CredentialsNotFound
    g.db = firestore.Client.from_service_account_json(credentials)


def get_db():
    if 'db' not in g:
        # print('error')
        # raise DBNotInitialized
        init_db()
    return g.db


def close_db(e=None):
    pass


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
