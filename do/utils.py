from flask import session
from datetime import date

from do import client, do_number, db
from do.models import User, Goal
from do.strings import daily_checkin_text


def sms_alert(message,recipient):
    '''
    sends a one-off sms to a user from do, expects message to be a string and
    recipient to be a phone number in format '+15554443333'
    '''
    phone_number = recipient
    body = f'{message}'
    client.messages.create(
                              body=body,
                              from_=do_number,
                              to=phone_number
                          )

def sms_broadcast(message,users=User.query.all()):
    '''
    for alerts: sends a one-off sms to multiple users from do, expects message
    to be a string and users to be a list of user IDs (default: all users)
    '''
    body = f'{message}'
    for user in users:
        phone_number = user.phone_number
        client.messages.create(
                              body=body,
                              from_=do_number,
                              to=phone_number
                          )

def daily_checkin():
    '''
    iterates through users in DB and sends a SMS to each one if the first goal
    associated with them is active
    '''
    today = date.today()
    weekday=today.strftime("%A")
    users = User.query.all()
    for user in users:
        goal = Goal.query.filter_by(user_id=user.id).first()
        if goal.active == True:
            body = daily_checkin_text(goal.description,weekday)
            phone_number = user.phone_number
            client.messages.create(
                                  body=body,
                                  from_=do_number,
                                  to=phone_number
                                  )
