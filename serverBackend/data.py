import threading


teams={}
teamDataLock = threading.Lock()
flags={}
flagsLock = threading.Lock()
progressDefault={
"loginpanel1":False
}
userDefault = {
"pass":"password"
}
mode = "jepardy"
# mode = "koth"
adminPass = ""
jwtKey = ""

def addTeam(teamName):
    teamDataLock.acquire()
    teams[team]={
    "members":{},
    "progress":progressDefault.copy()
    }
    teamDataLock.release()

def addMember(user,pwd,team):
    teamDataLock.acquire()
    teams[team]["members"][user] = userDefault
    teams[team]["members"][user]["pwd"] = pwd
    teamDataLock.release()
