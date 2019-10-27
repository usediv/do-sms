import unittest
from datetime import date, timedelta
today = date.today()

from do.strings import achievement_confirmation_text

class Test(unittest.TestCase):

    def test_achievement_confirmation_nil_all(self):
        streak=0
        count=0
        start_date = date(2019,7,1)
        result = achievement_confirmation_text(count,streak,start_date)
        self.assertEqual(result,"Nevermind! Today's a new day and another chance to achieve your goal!")

    def test_achievement_confirmation_on_the_board(self):
        streak=1
        count=1
        start_date = date(2019,7,1)
        result = achievement_confirmation_text(count,streak,start_date)
        self.assertEqual(result,"Great job! Congrats on achieving your first daily goal!")

    def test_achievement_confirmation_streaking(self):
        streak=2
        count=1
        start_date = date(2019,7,1)
        result = achievement_confirmation_text(count,streak,start_date)
        self.assertEqual(result,f"Nice work! That's {streak} days in a row and {count} days that you've achieved your goal in total. Keep up the good work!")

    def test_achievement_confirmation_fail(self):
        streak=0
        count=2
        start_date = date(2019,7,1)
        delta = today-start_date
        days = delta.days
        result = achievement_confirmation_text(count,streak,start_date)
        self.assertEqual(result,f"Nevermind! Today's a new day and another chance to achieve your goal! You've achieved your daily goal {count} times in {days} days.")

    def test_achievement_back_on_the_horse(self):
        streak=1
        count=2
        start_date = date(2019,7,1)
        delta = today-start_date
        days = delta.days
        result = achievement_confirmation_text(count,streak,start_date)
        self.assertEqual(result,f"Great job! Congrats on getting back on the horse! You've achieved your daily goal {count} times in {days} days.")



if __name__ == '__main__':
    unittest.main()
