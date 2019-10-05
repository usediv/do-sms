import os

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TWILIO_ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    DO_NUMBER = os.environ.get('DO_NUMBER')
