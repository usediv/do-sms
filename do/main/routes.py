from flask import request, session, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
from datetime import date

from do import db
from do.models import User, Goal, History
from do.strings import welcome_text, down_text, desc_prompt_text, more_or_less_error_text, make_or_break_error_text, goal_confirmation_text, goal_active_text, activation_error_text, achievement_confirmation_text
from do.utils import get_streak, get_count


main = Blueprint('main', __name__)

@main.route("/sms", methods=['GET', 'POST'])
def sms():

    # get number and message body
    number = request.form['From']
    text = request.form['Body']
    resp = MessagingResponse()
    today = date.today()

    # broad error handling
    try:

        # load user to check if in DB
        user = User.query.filter_by(phone_number=number).first()

        # if new user...
        if user==None:

            # add to db
            user = User(phone_number=number)
            db.session.add(user)
            db.session.commit()

            # welcome messaging and make or break prompt
            resp.message(welcome_text())

        # if existing user
        elif user!=None:

            # load goal to check if in DB
            goal=Goal.query.filter_by(user_id=user.id).first()

            # if no goal yet
            if goal==None:

                # catch if response is something other than MAKE or BREAK
                if text.lower()!='make' and text.lower()!='break':
                    resp.message(make_or_break_error_text())

                # if MAKE or BREAK received create new goal
                elif text.lower()=='make' or text.lower()=='break':
                    # save goal to DB without description
                    goal = Goal(goal_type=text.lower(),user_id=user.id)
                    db.session.add(goal)
                    db.session.commit()
                    # prompt for description
                    resp.message(desc_prompt_text(text.lower()))

            # if goal without description save description and send confirmation prompt
            elif goal!=None:

                # if MAKE or BREAK received create new goal
                if text.lower()=='make' or text.lower()=='break':
                    # save goal to DB without description
                    goal.goal_type=text.lower()
                    goal.description=None
                    goal.active=False
                    db.session.commit()
                    # prompt for description
                    resp.message(desc_prompt_text(text.lower()))

                # if goal without description, capture description
                elif goal.description==None:
                    goal.description=text
                    db.session.commit()
                    resp.message(goal_confirmation_text(text.lower(),goal.goal_type))

                # if goal with description
                elif goal.description!=None:

                    # but is not active (pending)
                    if goal.active==False:

                        #check for confirmation and activate if received
                        if text.lower()=='start':
                            goal.start_date=today
                            goal.active=True
                            db.session.commit()
                            resp.message(goal_active_text())

                        # if goal pending and other response received
                        elif text.lower()!='start':
                            resp.message(activation_error_text())

                    # if active goal
                    elif goal.active==True:

                        #load current history to check if in DB
                        current_history = History.query.filter_by(date=today, goal_id=goal.id).first()

                        # if goal response received
                        if text.lower()=='y' or text.lower()=='n':

                            # parse response based on goal type and update goal counters (if achieved)
                            if text.lower()=='y' and goal.goal_type=='make' or text.lower()=='n' and goal.goal_type=='break':
                                response=True

                            # if failed
                            elif text.lower()=='y' and goal.goal_type=='break' or text.lower()=='n' and goal.goal_type=='make':
                                response=False

                            # check if existing history item, update DB and respond
                            if current_history==None:
                                history = History(date = today, achieved=response, goal_id=goal.id)
                                db.session.add(history)
                            elif current_history!=None:
                                current_history.achieved = response
                            db.session.commit()

                            # send response
                            resp.message(achievement_confirmation_text(get_count(goal),get_streak(goal),goal.start_date,today))


    # if response fails send generic error message
    except:
        resp.message(down_text())

    return str(resp)
