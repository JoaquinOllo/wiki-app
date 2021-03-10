"""User

This script contains the model User class, along with a few methods for manipulating and validating users and passwords.
"""

from passlib.apps import custom_app_context as pwd_context
from flask import current_app
from Util import exceptions

class User:
    """
    A class used to represent users.
    ...

    Attributes
    ----------
    username : str
        The user login string.
    password_hash : str
        The encoded password.
    admin : bool
        A boolean indicating whether the user is an admin, or not.

    Methods
    -------
    hash_password(self, password)
        Returns the hashed password in a safe format for database storage
    verify_password(self, password)
        Returns true or false after comparing the password input with the stored password hash
    fromJSON(self, jsonInput)
        Sets the user attributes, from a json input, as extracted from the database
    toJSON(self)
        Returns a JSON equivalent of the object.
    """
    def __init__(self, username = "", password = "", admin = False, passwordHashed = False):
        self.username = username
        if (not passwordHashed):
            self.password_hash = self.hash_password(password)
        else:
            self.password_hash = password
        self.admin = admin


    def hash_password(self, password: str) -> str:
        """Returns the hashed password in a safe format for database storage
        ----------
        name : password
            A password string
        """ 
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Returns true or false after comparing the password input with the stored password hash
        ----------
        name : password
            A password string
        """
        return pwd_context.verify(password, self.password_hash)

    def fromJSON(self, jsonInput: object):
        """Sets the user attributes, from a json input, as extracted from the database
        Parameters
        ----------
        name : jsonInput
            A json provided as input
        """
        if (jsonInput):
            try:
                self.username = jsonInput["username"]
                self.password_hash = self.hash_password(jsonInput["password"])
            except KeyError:
                raise exceptions.InputError("Inadequate input json")

            try:
                self.admin = True if jsonInput["admin"] else False
            except:
                pass

    def toJSON(self) -> object :
        """Returns a JSON equivalent of the object.
        """

        newJSON = {
            "username": self.username,
            "password": self.password_hash,
            "admin": self.admin
        }

        return newJSON

    def validate(self) -> bool:
        #TODO complete
        """validates the user name and password
        """
        isUserValid = False

        return isUserValid

    def __str__(self):
        return "Username: {0}".format(self.username)

#newUser = User()
#newUser.fromJSON({"username": "user", "password":"password"})
#print(newUser)
#print(User().fromJSON({"username": "user"}))