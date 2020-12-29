from flask import jsonify, send_file, Blueprint, render_template, abort, request, g
import serverBackend.creds as creds
import os
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
adminPanel = Blueprint('adminPanel', __name__,
    template_folder=template_folder,
    static_folder=static_folder)

import serverBackend.data as data

@adminPanel.route('/',methods=['GET'])
def panel():
    return render_template("adminPanel.html")

@adminPanel.route('/addTeam',methods=['POST'])
def addTeam():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    team = request.form["team"]
    data.addTeam(team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/rmTeam',methods=['POST'])
def removeTeam():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    team = request.form["team"]
    if data.existTeam(team) == False:
        abort(400,"Invalid team given.")
    data.rmTeam(team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/addUser',methods=['POST'])
def addUser():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    user = request.form["user"]
    name = request.form["name"]
    comms = request.form["comms"]
    pwd = request.form["password"]
    team = request.form["team"]
    if data.existTeam(team) == False:
        abort(400)
    data.addMember(user,name,comms,pwd,team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/rmUser',methods=['POST'])
def removeUser():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    user = request.form["user"]
    team = request.form["team"]
    if data.existTeam(team) == False:
        abort("Invalid team given.",400)
    data.rmMember(user,team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/launch',methods=['POST'])
def launchGame():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    if data.gameStart:
        data.gameStart=False
        return "Game Stopped", 200
    else:
        data.gameStart=True
        return "Game Started", 200

@adminPanel.route('/data',methods=['POST'])
def getData():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    data.save()
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route("/history.log",methods=['POST'])
def logs():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    return send_file('./history.log')

@adminPanel.route("/registration.txt",methods=['POST'])
def registration():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    return send_file('./registration.txt')

@adminPanel.route('/loadData',methods=['POST'])
def loadData():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    manifest = request.form["manifest"]
    data.manifestLoad(manifest)
    scorebot.save()
    return send_file("."+os.sep+"serverData.json")
