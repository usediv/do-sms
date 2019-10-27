import unittest
from datetime import date, timedelta
today = date.today()

from do.strings import achievement_confirmation_text
from do.utils import get_count, get_streak, get_achieved
from do.models import User, Goal, History

class Test(unittest.TestCase):

    def test_achievement_confirmation_text(self):
        start_date = date(2019,7,1)
        delta = today-start_date
        days = delta.days
        self.assertEqual(achievement_confirmation_text(0,0,start_date),"Nevermind! Today's a new day and another chance to achieve your goal!")
        self.assertEqual(achievement_confirmation_text(1,1,start_date),"Great job! Congrats on achieving your first daily goal!")
        self.assertEqual(achievement_confirmation_text(3,2,start_date),"Nice work! That's 2 days in a row and 3 days that you've achieved your goal in total. Keep up the good work!")
        self.assertEqual(achievement_confirmation_text(2,0,start_date),f"Nevermind! Today's a new day and another chance to achieve your goal! You've achieved your daily goal 2 times in {days} days.")
        self.assertEqual(achievement_confirmation_text(2,1,start_date),f"Great job! Congrats on getting back on the horse! You've achieved your daily goal 2 times in {days} days.")

    def test_get_count(self):
        user = User(phone_number='+19999999999')
        goal = Goal(goal_type='make', user_id=user.id)
        history_1 = History(date=today, achieved=True, goal_id=goal.id)
        history_2 = History(date=today-timedelta(1), achieved=False, goal_id=goal.id)
        history_3 = History(date=today-timedelta(2), goal_id=goal.id)
        self.assertEqual(get_count([history_1,history_2,history_3]), 1)

    def test_get_streak(self):
        user = User(phone_number='+19999999999')
        goal = Goal(goal_type='make', user_id=user.id)
        history_1 = History(date=today, achieved=True, goal_id=goal.id)
        history_2 = History(date=today-timedelta(1), goal_id=goal.id)
        history_3 = History(date=today-timedelta(2), achieved=True, goal_id=goal.id)
        self.assertEqual(get_streak([history_1,history_2,history_3]), 1)
        self.assertEqual(get_streak([history_2,history_3]), 0)

    def test_get_achieved(self):
        user = User(phone_number='+19999999999')
        goal = Goal(goal_type='make', user_id=user.id)
        self.assertEqual(get_achieved(goal,'y'), True)
        self.assertEqual(get_achieved(goal,'n'), False)
        goal.goal_type='break'
        self.assertEqual(get_achieved(goal,'n'), True)
        self.assertEqual(get_achieved(goal,'y'), False)


if __name__ == '__main__':
    unittest.main()
