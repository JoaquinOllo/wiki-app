from passlib.apps import custom_app_context as pwd_context
from flask import current_app

class User:
    def __init__(self, username, password, admin = False):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.admin = admin


    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)