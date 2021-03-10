from datetime import datetime, timedelta
from Engine.dbconnection import myclient

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours = 2)
    SESSION_COOKIE_NAME = "session"
    SESSION_MONGODB = myclient
    SESSION_TYPE = "mongodb"
    SESSION_MONGODB_DB	= "flask_session"
    SESSION_MONGODB_COLLECT = "sessions"

config = {
    'development': DevelopmentConfig,
}