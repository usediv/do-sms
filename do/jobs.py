from do import account_sid, auth_token, client, do_number
from do.utils import daily_checkin

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=12, minute=50)
def scheduled_job():
    print('Scheduler running')
    daily_checkin()

sched.start()
