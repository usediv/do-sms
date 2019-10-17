from datetime import date, timedelta
today = date.today()

def welcome_text():
    return "Welcome to Do! Do is an SMS app that can help you make or break habits by tracking your progress daily. Do you want help to make a new habit or break a bad one? Reply with either MAKE or BREAK to get started"

def down_text():
    return "Sorry, Do isn't available right now. Please try again later"

def desc_prompt_text(goal_type):
    if goal_type.lower()=='make':
        amount='more'
        egs='Exercise? Read? Practice the piano?'
    elif goal_type.lower()=='break':
        amount='less'
        egs='Drink? Swear? Eat junk food?'
    return f"OK, what do you want to do {amount} often? {egs}"

def more_or_less_error_text():
    return "Please only respond with MAKE or BREAK"

def make_or_break_error_text():
    return "Please only reply MAKE or BREAK"

def goal_confirmation_text(goal, goal_type):
    if goal_type=='make':
        frequency='more often'
    elif goal_type=='break':
        frequency='less often'
    return f"OK great! You want to {goal} {frequency}. To start receiving daily texts from Do reply START. You can text MAKE or BREAK to change your goal or STOP to stop receiving texts at any time"

def goal_active_text():
    return "Ok, you'll start receiving daily texts from tomorrow. Good luck for your first day!"

def activation_error_text():
    return "Reply START to begin receiving daily texts"

def daily_checkin_text(goal, weekday):
    return f"Happy {weekday}! Did you {goal} yesterday? Reply Y for yes or N for no"

def achievement_confirmation_text(count,streak,start_date,today=today):
    delta = today-start_date
    days = delta.days
    if streak==0 and count==0:
        return "Nevermind! Today's a new day and another chance to achieve your goal!"
    elif streak==1 and count==1:
        return "Great job! Congrats on achieving your first daily goal!"
    elif streak==0 and count>=1:
        return f"Nevermind! Today's a new day and another chance to achieve your goal! You've achieved your daily goal {count} times in {days} days."
    elif streak==1 and count>1:
        return f"Great job! Congrats on getting back on the horse! You've achieved your daily goal {count} times in {days} days."
    elif streak>=2:
        return f"Nice work! That's {streak} days in a row and {count} days that you've achieved your goal in total. Keep up the good work!"
