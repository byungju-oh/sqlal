import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://ubuntu:ubuntu@34.45.34.202/data'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)