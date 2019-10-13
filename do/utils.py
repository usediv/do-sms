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
    Iterates through users in DB and sends a SMS to each one if the first goal
    associated with them is active
    '''
    today = date.today()
    weekday=today.strftime("%A")
    users = User.query.all()
    # iterate through users
    for user in users:
        print(user)
        goal = Goal.query.filter_by(user_id=user.id).first()
        # check if goal is active
        if goal.active == True:
            print('active')
            # check yesterday to see if response recorded
            yesterday = History.query.filter_by(date=today-timedelta(days=1), goal_id=goal.id).first()
            print(yesterday)
            #avoid error if no record for yesterday
            if yesterday!=None:
                if yesterday.achieved==None:
                    # reset streak to zero if not
                    goal.streak=0
            # check for history item for today (safeguard: redundant in normal cases)
            current_history = History.query.filter_by(date=today, goal_id=goal.id).first()
            if current_history==None:
                # create history item
                history = History(date = today, goal_id=goal.id)
                db.session.add(history)
                # commit to db
                db.session.commit()
            # # compose and send message
            # body = daily_checkin_text(goal.description,weekday)
            # phone_number = user.phone_number
            # client.messages.create(
            #                       body=body,
            #                       from_=do_number,
            #                       to=phone_number
            #                       )

def get_streak(goal,date=date.today(),counter=0):
    """
    checks DB and returns number of continuous days a goal is marked as achieved
    counting back from the date passed (default today)
    """
    history = History.query.filter_by(date=date, goal_id=goal.id).first()
    if history==None or history.achieved==False or history.achieved==None:
        return counter
    else:
        return (get_streak(goal,date-timedelta(days=1),counter+1))

def get_count(goal,date=date.today(),counter=0):
    """
    checks DB and returns totalnumber of days a goal is marked as achieved
    counting back from the date passed (default today)
    """
    history = History.query.filter_by(date=date, goal_id=goal.id).first()
    if history!=None and history.achieved==True:
        counter+=1
    if date<=goal.start_date:
        return counter
    else:
        return (get_count(goal,date-timedelta(days=1),counter))
