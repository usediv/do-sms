from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from twilio.rest import Client

from do.config import Config


app = Flask('__name__')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# for sending texts (not necessary for responding)
account_sid = Config.TWILIO_ACCOUNT_SID
auth_token = Config.TWILIO_AUTH_TOKEN
client = Client(account_sid,auth_token)
do_number = Config.DO_NUMBER

from do.main.routes import main
# app.register_blueprint(main)
