from flask import session
from datetime import date, timedelta

from do import client, do_number, db
from do.models import User, Goal, History
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
    for alerts: sends a one-off sms to multiple users from Do if they have an
    active goal, expects message to be a string and users to be a list of user
    IDs (default: all users)
    '''
    body = f'{message}'
    for user in users:
        goal = Goal.query.filter_by(user_id=user.id).first()
        # check if goal is active
        if goal!=None and goal.active == True:
            # send message
            phone_number = user.phone_number
            client.messages.create(
                                  body=body,
                                  from_=do_number,
                                  to=phone_number
                              )

def daily_checkin():
    '''
    Iterates through users in DB and sends a SMS to each one if the first goal
    associated with them is active
    '''
    today = date.today()
    weekday=today.strftime("%A")
    users = User.query.all()
    # iterate through users
    for user in users:
        goal = Goal.query.filter_by(user_id=user.id).first()
        # check if goal is active
        if goal!=None and goal.active == True:
            # check for history item for today (safeguard: redundant in normal cases)
            current_history = History.query.filter_by(date=today, goal_id=goal.id).first()
            if current_history==None:
                # create history item
                history = History(date=today, goal_id=goal.id)
                db.session.add(history)
                # commit to db
                db.session.commit()
            # compose and send message
            body = daily_checkin_text(goal.description,weekday)
            phone_number = user.phone_number
            client.messages.create(
                                  body=body,
                                  from_=do_number,
                                  to=phone_number
                                  )

def get_achieved(goal,response):
    """
    takes in a goal and achievement response and returns if goal was achieved
    or not as boolean based on goal type (eg. 'y' + 'make' = True)
    """

    if goal.goal_type=='make':
        if response.lower()=='y' or response.lower()=='yes':
            return True
        if response.lower()=='n' or response.lower()=='no':
            return False
    if goal.goal_type=='break':
        if response.lower()=='n' or response.lower()=='no':
            return True
        if response.lower()=='y' or response.lower()=='yes':
            return False



def get_streak(histories):
    """
    takes in a list of histories and returns number of times goal was achieved
    in a row as an integer, working backwards from latest to earliest
    """
    histories = sorted(histories, key=lambda history: history.date, reverse=True)
    streak = 0
    for history in histories:
        if history.achieved==True:
            streak+=1
        else:
            return streak
    return streak

def get_count(histories):
    """
    takes in a list of histories and returns total number of days a goal is
    marked as achieved as an integer
    """
    count = 0
    for history in histories:
        if history.achieved==True:
            count+=1
    return count
