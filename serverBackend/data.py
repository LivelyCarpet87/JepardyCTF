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

currentUser = ""
currentUserTeam = ""

gameConstants = jsonFile("Data/Current/gameConstants.json")

def refresh():
	global gameConstants
	gameConstants = jsonFile("Data/Current/gameConstants.json")
	updateLockDict()

def jsonFile(relPath):
	f = open(os.path.join(os.getcwd(),os.path.normpath(relPath)))
	d = json.loads(f.read())
	f.close()
	return d

def saveJsonFile(relPath,contents):
	f = open(os.path.join(os.getcwd(),os.path.normpath(relPath)),"w")
	d = json.dumps(contents, indent=4)
	f.write(d)
	f.close()

def getLockPath(relPath):
	return os.path.join(os.getcwd(),"Data","Current",os.path.normpath(relPath))+".lock"

lockDict={
	"gameConstants": FileLock(getLockPath("gameConstants")),
	"challengesMaster": FileLock(getLockPath("Challenges/challengesMaster.json")),
	"teamsMaster": FileLock(getLockPath("Teams/teamsMaster.json"))
}

def updateLockDict():
	teamsMaster = jsonFile("Data/Current/Teams/teamsMaster.json")
	for team in teamsMaster["existingTeams"]:
		if team not in lockDict.keys():
			lockDict[team] = FileLock(getLockPath("Teams/"+team))
	challengesMaster = jsonFile("Data/Current/Challenges/challengesMaster.json")
	for challenge in challengesMaster["ExistingChallengeTypes"]:
		if challenge not in lockDict.keys():
			lockDict[challenge] = FileLock(getLockPath("Challenges/"+challenge))

# Clients: Challenges
# Marks a challenge as completed for the team (Jepardy storage) and marks the team as the king for the specified challenge (KotH storage)
# Will lock teams file for the jepardy storage
# Locks challengeGlobal file for the koth storage
# Calls setChallengeProgress(Locks)
# Returns none
def solveChallenge(team,challengeName,type):
	timeStr=datetime.datetime.now().isoformat()
	lockDict[team].acquire()
	d = jsonFile("Data/Current/Teams/"+team+".json")
	if challengeName not in d["solved"].keys():
		d["solved"][challengeName]=timeStr
	saveJsonFile("Data/Current/Teams/"+team+".json",d)
	lockDict[team].release()
	del d
	lockDict[type].acquire()
	d = jsonFile("Data/Current/Challenges/"+type+".json")
	if d[challengeName]["controlledBy"]!=team:
		d[challengeName]["controlledBy"]=team
		d[challengeName]["timeOfLastTakeover"]=timeStr
	saveJsonFile("Data/Current/Challenges/"+type+".json",d)
	lockDict[type].release()

# Clients: Challenges, solveChallenge
# Returns the state of the challenge for the team from the Jepardy storage
def getChallengeProgress(team,challengeName,type):
	if gameConstants["mode"] == 1:
		d = jsonFile("Data/Current/Teams/"+team+".json")
		return (challengeName in d["solved"].keys())
	elif gameConstants["mode"] == 2:
		d = jsonFile("Data/Current/Challenges/"+type+".json")
		return d[challengeName]["controlledBy"]==team

def checkFlag(type,challengeName,flagIn):
	d = jsonFile("Data/Current/Challenges/"+type+".json")
	return d[challengeName]["flag"]==flagIn

def addTeam(teamName):
	d = gameConstants["defaultTeamData"].copy()
	d["name"]=teamName
	saveJsonFile("Data/Current/Teams/"+teamName+".json",d)
	del d
	lockDict["teamsMaster"].acquire()
	d = jsonFile("Data/Current/Teams/teamsMaster.json")
	if teamName not in d["existingTeams"]:
		d["existingTeams"].append(teamName)
		saveJsonFile("Data/Current/Teams/teamsMaster.json",d)
	lockDict["teamsMaster"].release()

def rmTeam(team):
	lockDict["teamsMaster"].acquire()
	d = jsonFile("Data/Current/Teams/teamsMaster.json")
	if teamName in d["existingTeams"]:
		d["existingTeams"].remove(teamName)
		saveJsonFile("Data/Current/Teams/teamsMaster.json",d)
	lockDict["teamsMaster"].release()

def addMember(user,name,comms,pwd,team):
	u = gameConstants["defaultMemberData"].copy()
	u["name"]=name
	u["comms"]=comms
	u["pwd"]=pwd
	lockDict[team].acquire()
	d=jsonFile("Data/Current/Teams/"+team+".json")
	d["members"][user]=u
	saveJsonFile("Data/Current/Teams/"+team+".json",d)
	lockDict[team].release()

def rmMember(user,team):
	lockDict[team].acquire()
	d=jsonFile("Data/Current/Teams/"+team+".json")
	del d["members"][user]
	saveJsonFile("Data/Current/Teams/"+team+".json",d)
	lockDict[team].release()
