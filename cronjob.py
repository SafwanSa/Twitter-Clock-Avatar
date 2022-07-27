# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
from main import cronjob

scheduler = BlockingScheduler()
scheduler.add_job(cronjob, "interval", seconds=300)
scheduler.start()