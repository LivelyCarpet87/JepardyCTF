import threading, datetime, logging, os
import serverBackend.serverExceptions
import serverBackend.creds as creds
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
teamDataLock = threading.Lock()
flags={}
flagsLock = threading.Lock()
progressDefault={
"loginpanel1":False
}
userDefault = {
"name":"",
"pass":"password"
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

def addTeam(teamName):
    teamDataLock.acquire()
    teams[team]={
    "members":{},
    "progress":progressDefault.copy(),
    "score":0,
    "lastScoreIncrease":datetime.datetime.now().isoformat()
    }
    teamDataLock.release()

def rmTeam(teamName):
    teamDataLock.acquire()
    del teams[team]
    teamDataLock.release()

def addMember(user,name,pwd,team):
    teamDataLock.acquire()
    teams[team]["members"][user] = userDefault
    teams[team]["members"][user]["name"] = name
    teams[team]["members"][user]["pwd"] = pwd
    teamDataLock.release()

def rmMember(user,team):
    teamDataLock.acquire()
    del teams[team]["members"][user]
    teamDataLock.release()

def manifestUpdate():
    global teams, flags, mode, progressDefault, userDefault, adminPass, jwtKey, gameStart, scorebotInterval, modifierDivider, gameUptime, hintReleaseCycle
    manifest = {
    "teams":teams,
    "flags":flags,
    "mode":mode,
    "progressDefault":progressDefault,
    "userDefault":userDefault,
    "adminPass":creds.adminPass,
    "jwtKey":creds.jwtKey,
    "gameStart":gameStart,
    "modifierDivider":modifierDivider,
    "scorebotInterval":scorebotInterval,
    "gameUptime":gameUptime,
    "hintReleaseCycle":hintReleaseCycle
    }

def manifestLoad(manifest):
    global teams, flags, mode, progressDefault, userDefault, adminPass, jwtKey, gameStart, scorebotInterval, modifierDivider, gameUptime, hintReleaseCycle
    manifest = json.loads(manifest)
    teams = manifest.get("teams",teams)
    flags = manifest.get("flags",flags)
    jwtKey = manifest.get("jwtKey",creds.jwtKey)
    adminPass = manifest.get("adminPass",creds.adminPass)
    gameStart = manifest.get("gameStart",gameStart)
    modifierDivider = manifest.get("modifierDivider",modifierDivider)
    scorebotInterval = manifest.get("scorebotInterval",scorebotInterval)
    gameUptime = manifest.get("gameUptime",gameUptime)
    hintReleaseCycle = manifest.get("hintReleaseCycle",hintReleaseCycle)
    scorebot.scheduler.reschedule_job('scorebot',trigger="interval", seconds=scorebotInterval)
