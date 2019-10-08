from flask import request, session, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
import locale

locale.setlocale( locale.LC_ALL, '' )

from do import db
from do.models import User, Goal
from do.strings import welcome_text, down_text, more_text, less_text, more_or_less_error_text, make_or_break_error_text, goal_confirmation_text, goal_active_text, activation_error_text


main = Blueprint('main', __name__)

@main.route("/sms", methods=['GET', 'POST'])
def sms():

    # get number and message body
    number = request.form['From']
    text = request.form['Body']
    resp = MessagingResponse()

    # broad error handling
    try:

        # query db to check if user exists
        user = User.query.filter_by(phone_number=number).first()

        # if new user...
        if user == None:
            print('No user')

            # add to db
            user = User(phone_number=number)
            db.session.add(user)
            db.session.commit()

            # welcome messaging and make or break prompt
            resp.message(welcome_text())
            session['new_goal'] = 'new'

        # if MAKE or BREAK received save session
        elif text.lower()=='make' or text.lower()=='break':
            session['new_goal'] = text.lower()
            if text.lower()=='make':
                resp.message(more_text())
            elif text.lower()=='break':
                resp.message(less_text())

        # catch if trying something other than make or break for new user
        elif session['new_goal']=='new':
            if text.lower()!='make' or text.lower()!='break':
                resp.message(make_or_break_error_text())

        # if new goal capture description and save as inactive/pending
        elif session['new_goal']=='make' or session['new_goal']=='break':
            goal = Goal.query.filter_by(user_id=user.id).first()
            # if user doesn't have goal yet create new one
            if goal == None:
                goal = Goal(goal_type=session['new_goal'],description=text,active=False,user_id=user.id)
                db.session.add(goal)
            #if user already has a goal update it
            else:
                goal.goal_type=session['new_goal']
                goal.description=text
                goal.active=False
            db.session.commit()
            resp.message(goal_confirmation_text(text.lower(),session['new_goal']))
            session['new_goal']='pending'

        # if new goal is pending and confirmation received
        elif session['new_goal']=='pending' and text.lower()=='start':
            goal = Goal.query.filter_by(user_id=user.id).first()
            goal.active=True
            db.session.commit()
            resp.message(goal_active_text())
            session['new_goal']='complete'

        # if goal pending and other response received
        elif session['new_goal']=='pending' and text.lower()!='start':
            resp.message(activation_error_text())

    # if response fails send generic error message
    except:
        resp.message(down_text())

    return str(resp)
