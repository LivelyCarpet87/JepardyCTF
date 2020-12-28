import threading
import datetime
import logging
import os
import json
import apscheduler
from filelock import Timeout, FileLock

import serverBackend.serverExceptions
import serverBackend.creds as creds
import serverBackend.scorebot as scorebot

log = logging.getLogger('CTF')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(os.getcwd() + os.sep + 'history.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)
fh = logging.FileHandler(os.getcwd() + os.sep + 'historyINFO.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
log.addHandler(fh)

teams={}
flags={}


progressDefault={
"loginpanel1":False
}
userDefault = {
"name":"",
"pwd":"password"
}
mode = "jepardy"
# mode = "koth"
gameStart = False
scorebotInterval=60
modifierDivider=3600
gameUptime=0
hintReleaseCycle=4*3600

manifest = {
"teams":teams,
"flags":flags,
"mode":mode,
"progressDefault":progressDefault,
"userDefault":userDefault,
"gameStart":gameStart,
"modifierDivider":modifierDivider,
"scorebotInterval":scorebotInterval,
"adminPass":creds.adminPass,
"jwtKey":creds.jwtKey,
"gameUptime":gameUptime,
"hintReleaseCycle":hintReleaseCycle
}

# Clients: Challenges
# Marks a challenge as completed for the team (Jepardy storage) and marks the team as the king for the specified challenge (KotH storage)
# Will lock teams file for the jepardy storage
# Locks challengeGlobal file for the koth storage
# Calls setChallengeProgress(Locks)
# Returns none
def solveChallenge(team,challengeName):
	pass

# Clients: Challenges, solveChallenge
# Returns the state of the challenge for the team from the Jepardy storage
def getChallengeProgress(team,challengeName):
	pass

# Clients: solveChallenge
# Marks a challenge as needed for the team (Jepardy storage)
# returns none
def setChallengeProgress(team,challengeName,progress):
	pass

def addTeam(team):
	pass

def rmTeam(team):
	pass

def addMember(user,name,pwd,team):
	pass

def rmMember(user,team):
	pass

def manifestLoad(manifest):
	pass

def save():
	pass

def load():
	pass
