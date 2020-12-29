import serverBackend.data as data
import json
import os
import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler
from filelock import Timeout, FileLock
import atexit

def tallyScore():
	pass

def maintainers():
	pass

def incrementCounter():
	data.incrementUptime()

def job_function():
	now = datetime.datetime.now()
	early = now.replace(hour=7, minute=45, second=0, microsecond=0)
	late = now.replace(hour=22, minute=30, second=0, microsecond=0)
	if data.getConstant("gameStart") and (now > early or now < late):
		incrementCounter()
		tallyScore()
		maintainers()
	refresh()

def backup():
	#data.log.debug("Server data saved. ")
	now = datetime.datetime.now()

runScorebot = FileLock(os.path.join(os.getcwd(),"Data","scorebot.lock"), timeout=1)
runBackup = FileLock(os.path.join(os.getcwd(),"Data","backupbot.lock"), timeout=1)

def init():
	data.refresh()
	interval = data.getConstant("scorebotInterval")
	try:
		runScorebot.acquire()
		scheduler.add_job(func=job_function, trigger="interval", seconds=interval, id='scorebot')
		data.log.debug("Scorebot Started")
	except Timeout:
		data.log.debug("Scorebot Already Started")

	try:
		runBackup.acquire()
		scheduler.add_job(func=backup, trigger="interval", seconds=3600, id='backup')
	except Timeout:
		pass

@atexit.register
def releaseLocks():
	runScorebot.release(force=True)
	runBackup.release(force=True)

scheduler = BackgroundScheduler()
scheduler.start()
