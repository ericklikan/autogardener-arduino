import os
import pyrebase
import requests

from .firebase_config import config
from .store.store import store, retrieve


class Firebase:
    user = None

    def __init__(self):
        self.config = config
        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()

        if os.path.isfile('config.json'):
            self.__refresh_user()
        else:
            self.setup_new_user()

    def update_data(self, data_type, data):
        try:
            self.db.child("users").child(retrieve("userid")).update({data_type: data})
        except requests.exceptions.HTTPError as e:
            print(e)
            self.__refresh_user()
            self.update_data(data_type, data)

    def setup_new_user(self):
        # Assume username and password are on environment variables that they got during setup
        email = os.environ.get('FIREBASE_USER') or ""
        store('user_email', email)

        # Password is only needed for first login, refresh token will reauth for us
        password = os.environ.get('FIREBASE_PW') or ""

        print(email)
        print(password)

        try:
            self.user = self.auth.sign_in_with_email_and_password(email, password)
            store('refreshToken', self.user['refreshToken'])
            store('userid', self.user['localId'])

        except (requests.exceptions.HTTPError, TypeError) as e:
            print(e)
            os.remove('config.json')
            return False

    def __refresh_user(self):
        self.user = self.auth.refresh(retrieve('refreshToken'))
