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

    # try:
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

    # save session and goal prompt
    elif text.lower()=='make' or text.lower()=='break':
        session['new_goal'] = text.lower()
        if text.lower()=='make':
            resp.message(more_text())
        elif text.lower()=='break':
            resp.message(less_text())

    #catch if trying something other than make or break entered
    elif session['new_goal']=='new' and text.lower()!='make' or session['new_goal']=='new' and text.lower()!='break':
        resp.message(make_or_break_error_text())

    # capture description if creating a new goal
    elif session['new_goal']=='make' or session['new_goal']=='break':
        goal = Goal(goal_type=session['new_goal'],description=text,user_id=user.id)
        db.session.add(goal)
        db.session.commit()
        resp.message(goal_confirmation_text(text.lower(),session['new_goal']))
        session['new_goal']='pending'

    elif session['new_goal']=='pending' and text.lower()=='start':
        goal = Goal.query.filter_by(user_id=user.id).first()
        goal.active=True
        db.session.commit()
        resp.message(goal_active_text())
        session['new_goal']='complete'

    elif session['new_goal']=='pending' and text.lower()!='start':
        resp.message(activation_error_text())



            # # if neither, error
            # else:
            #     resp.message(more_or_less_error_text())

        # # check if goal has a description
        # elif Goal.query.filter_by(user_id=user.id).first().description==None:
        #     resp.message('Nothing to see here')
        # elif Goal.query.filter_by(user_id=user.id).first().description == None:

            # if no goal and have specified make or break, save goal
            # else:

                # goal = Goal(description=text,user_id=user.id)
                # db.session.add(goal)
                # db.session.commit()
                #
                # # goal confirmation messaging
                # print('New goal ' + description)


# # otherwise check if user has a goal
# elif Goal.query.filter_by(user_id=user.id).first() == None:

# goal = Goal(goal_type='more',user_id=user.id)
# db.session.add(goal)
# db.session.commit()

            # goal = Goal(goal_type='less')
            # db.session.add(goal)
            # db.session.commit()

        #     if text.lower() == 'idk':
        #         resp.message("To figure out your weekly spending budget take your annual income, minus expenses (any costs that you know you’ll incur throughout the year), and divide that by 52")
        #         resp.message("This will tell you roughly how much you can spend each week without going into debt")
        #         resp.message("Decide how much of this you want to allow for spending and the rest is your savings!")
        #         resp.message("Try to pick an amount for your weekly spending budget that allows some room for larger purchases (like travel or gifts)")
        #         resp.message("Any left over spending budget at the end of the week will roll over into following weeks’ budgets, allowing you to cover larger purchases without breaking your budget.")
        #         resp.message("What would you like your weekly spending budget to be?")
        #
        #     else:
        #
        #         try:
        #             budget = Budget(budget=float(text),balance=float(text),user_id=user.id)
        #             db.session.add(budget)
        #             user.active = True
        #             db.session.commit()
        #             resp.message("Great!")
        #             resp.message("Send me the dollar amount when you pay for things (that you didn't budget as an expense) and I’ll help you keep track of how much spending budget you have left for the week")
        #             resp.message("Your remaining weekly spending budget is {}".format(locale.currency(text, grouping=True)))
        #             print('Budget set ' + number)
        #
        #         except:
        #             resp.message("Sorry, please only reply with either a number or 'idk' if you’re not sure what your weekly spending budget should be")
        #             resp.message("What would you like your weekly spending budget to be?")
        #
        # # if not a new user and has a spending budget...
        # else:
        #
        #     # check if the user is trying to stop mo texts
        #     if text.lower == 'stop':
        #         try:
        #             resp.message("You'll no longer receive texts")
        #         except:
        #             resp.message("Wut")
        #
        #     # otherwise confirm spending
        #     else:
        #
        #         try:
        #             budget = Budget.query.filter_by(user_id=user.id).first()
        #             balance = budget.balance
        #             updatedBalance = balance - float(text)
        #             budget.balance = updatedBalance
        #             db.session.commit()
        #             if updatedBalance < 0:
        #                 updatedBalance = 0
        #             resp.message("Your remaining weekly spending budget is {}".format(locale.currency(updatedBalance, grouping=True)))
        #             print('Spending recorded ' + number)
        #
        #         except:
        #             resp.message("Sorry, please only reply with a number to record spending")
        #             resp.message("Your remaining weekly spending budget is {}".format(locale.currency(balance, grouping=True)))

    # except:
    #     resp.message(down_text())

    return str(resp)
