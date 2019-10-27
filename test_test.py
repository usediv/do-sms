import unittest
from datetime import date, timedelta
today = date.today()

from do.strings import achievement_confirmation_text

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


if __name__ == '__main__':
    unittest.main()
