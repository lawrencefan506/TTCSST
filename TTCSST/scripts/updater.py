#Scheduled task

from apscheduler.schedulers.background import BackgroundScheduler
from .tracker import tracker

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tracker, 'interval', minutes=15)
    scheduler.start()