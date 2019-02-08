from google.cloud import firestore
from exception import DBNotInitialized, CredentialsNotFound
import os
from flask import current_app

credentials = os.path.split(os.path.realpath(__file__))[0]
credentials = os.path.join(credentials, 'credentials', 'yummy-g08-807d7ab294cf.json')
print(credentials)

def init_db():
    from flask import g
    if not os.path.exists(credentials):
        raise CredentialsNotFound
    g.db = firestore.Client.from_service_account_json(credentials)


@current_app.app_context
def get_db():
    from flask import g

    if 'db' not in g:
        raise DBNotInitialized

    return g.db