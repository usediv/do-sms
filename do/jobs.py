from do import account_sid, auth_token, client, do_number
from do.utils import daily_checkin

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=0)
def scheduled_job():
    daily_checkin()

sched.start()
