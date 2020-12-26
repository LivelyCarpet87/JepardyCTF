import serverBackend.data as data
import json
import os
import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler

def incrementCounter():
	data.gameUptime += data.scorebotInterval

def tallyScore():
    pass

def maintainers():
    pass

def save():
	#data.log.debug("Server data saved. ")
	with open("."+os.sep+'serverData.json', 'w') as f:
		data.manifestUpdate()
		json.dump(data.manifest, f, default=lambda x: None)

def job_function():
	now = datetime.datetime.now()
	early = now.replace(hour=7, minute=45, second=0, microsecond=0)
	late = now.replace(hour=22, minute=30, second=0, microsecond=0)
	if data.gameStart and (now > early or now < late):
		incrementCounter()
		tallyScore()
		maintainers()
	save()

def backup():
	#data.log.debug("Server data saved. ")
	now = datetime.datetime.now()
	with open("."+os.sep+'backups'+os.sep+repr(now)+'.serverData.bak.json', 'w') as f:
		data.manifestUpdate()
		json.dump(data.manifest, f, default=lambda x: None)

def init():
	interval = data.scorebotInterval
	scheduler.add_job(func=job_function, trigger="interval", seconds=interval, id='scorebot')
	data.log.debug("Scorebot Started")
	scheduler.add_job(func=backup, trigger="interval", seconds=3600, id='backup')


scheduler = BackgroundScheduler()
scheduler.start()
