def welcome_text():
    return "Welcome to Do! Do is an SMS app that can help you make good habits or break bad ones by tracking your progress daily. Do you want help to make a new habit or break a bad one? Reply with either MAKE or BREAK to get started"

def down_text():
    return "Sorry, Do isn't available right now. Please try again later"

def more_text():
    return "OK, what do you want to do more often? Exercise? Read? Practice the piano?"

def less_text():
    return "OK, what do you want to do less often? Drink? Swear? Eat junk food?"

def more_or_less_error_text():
    return "Please only respond with MAKE or BREAK"

def make_or_break_error_text():
    return "Please only reply MAKE or BREAK"

def goal_confirmation_text(goal, goal_type):
    if goal_type=='make':
        frequency='more often'
    elif goal_type=='break':
        frequency='less often'
    return f"OK, you want to {goal} {frequency}. Great! To start receiving daily texts from Do reply START. You can text MAKE or BREAK to change your goal or STOP to stop receiving texts at any time"

def goal_active_text():
    return "Ok, you'll start receiving daily texts tomorrow. Good luck for your first day!"

def activation_error_text():
    return "Reply START to begin receiving daily texts"

def daily_checkin_text(goal, weekday):
    return f"Happy {weekday}! Did you {goal} yesterday? Reply Y for yes or N for no"
