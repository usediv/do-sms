from flask import request, session, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
import locale

locale.setlocale( locale.LC_ALL, '' )

from do import db
from do.models import User, Goal
from do.strings import welcome_text, down_text, more_text, less_text, more_or_less_error_text


main = Blueprint('main', __name__)

@main.route("/sms", methods=['GET', 'POST'])
def sms():

    # get number and message body
    number = request.form['From']
    text = request.form['Body']
    resp = MessagingResponse()

    try:
        # query db to check if user exists
        user = User.query.filter_by(phone_number=number).first()

        # if new user...
        if user == None:

            # add to db
            user = User(phone_number=number)
            db.session.add(user)
            db.session.commit()

            # welcome messaging and make or break prompt
            resp.message(welcome_text())

        # otherwise check if user has a goal
        elif Goal.query.filter_by(user_id=user.id).first() == None:

            # if no goal and replied 'make', create a more goal
            if text.lower()=='make':
                goal = Goal(goal_type='more')
                db.session.add(goal)
                db.session.commit()
                resp.message(more_text())

            # if no goal and replied 'break', create a less goal
            elif text.lower()=='break':
                goal = Goal(goal_type='less')
                db.session.add(goal)
                db.session.commit()
                resp.message(less_text())

            # if neither, error
            else:
                resp.message(more_or_less_error_text())

        # check if goal has a description
        elif Goal.query.filter_by(user_id=user.id).first().description==None:
            resp.message('Nothing to see here')
        # elif Goal.query.filter_by(user_id=user.id).first().description == None:

            # if no goal and have specified make or break, save goal
            else:

                # goal = Goal(description=text,user_id=user.id)
                # db.session.add(goal)
                # db.session.commit()
                #
                # # goal confirmation messaging
                # print('New goal ' + description)




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

    except:
        resp.message(down_text())

    return str(resp)
