from flask import session

from do import client, do_number, db
from do.models import User, Goal
# from do.strings import sunday_summary_text


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

def sms_broadcast(message,users=User.query.filter_by(active=True).all()):
    '''
    for alerts: sends a one-off sms to multiple users from do, expects message
    to be a string and users to be a list of user IDs (default: all active users)
    '''
    body = f'{message}'
    for user in users:
        phone_number = user.phone_number
        client.messages.create(
                              body=body,
                              from_=do_number,
                              to=phone_number
                          )

# def sunday_summary():
#     '''
#     resets ALL users' spending budgets (even if inactive) and notifies them if active
#     '''
#     users = User.query.all()
#     for user in users:
#         budget = Budget.query.filter_by(user_id=user.id).first()
#         newBalance = budget.budget
#         budget.balance = newBalance
#         db.session.commit()
#         if user.active == True:
#             body = sunday_summary_text(newBalance)
#             phone_number = user.phone_number
#             client.messages.create(
#                                   body=body,
#                                   from_=mo_number,
#                                   to=phone_number
#                                   )
