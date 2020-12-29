import flask
from flask import jsonify, send_file, Blueprint, render_template, abort, request, g, make_response


from . import panel0, panel1, panel2
from serverBackend import data

import os

type="loginPanels"
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
loginpanels = Blueprint(type, __name__,
						template_folder=template_folder,
						static_folder=static_folder)

data.enrollChallengeType(type)

@loginpanels.route('/',methods=['GET'])
def base():
	return render_template("LoginPanelsListing.html")

# Panel 0: Sanity Test
data.enrollChallenge("loginPanels",panel0.name,"N/A",
{
    "1": "This page is just a sanity test.",
    "2": "Just try entering anything!",
    "3": "Why would you ever need more hints?"
},
0,{
    "filter":{}
})

@loginpanels.route('/panel0',methods=['GET','POST'])
def viewPanel0():
	if flask.request.method == 'GET':
		debugMode = request.cookies.get('Panel0DebugMode',"0")
		response = make_response(
			render_template("LoginPanels.html",
				panel=0,
				solved=data.getChallengeProgress(data.currentUserTeam,panel0.name,type),
				debugMode=debugMode,
				debug="N/A"
			)
		)
		response.set_cookie('Panel0DebugMode', debugMode)
		return response
	elif flask.request.method == 'POST':
		debugMode = request.cookies.get('Panel0DebugMode',"0")
		user = request.form["user"]
		pwd = request.form["pwd"]
		success, debug, message = panel0.panel0(user,pwd)
		if success:
			data.solveChallenge(data.currentUserTeam,panel0.name,type)
		return render_template("LoginPanels.html",
			panel=0,
			solved=data.getChallengeProgress(data.currentUserTeam,panel0.name,type),
			debugMode=debugMode,
			debug=debug,
			message=message
		)

# Panel 1: Default Creds
data.enrollChallenge("loginPanels",panel1.name,"N/A",
{
    "1": "Defaults."
},
50,{
    "filter":{}
})

@loginpanels.route('/panel1',methods=['GET','POST'])
def viewPanel1():
	if flask.request.method == 'GET':
		debugMode = request.cookies.get('Panel1DebugMode',"0")
		response = make_response(
			render_template("LoginPanels.html",
				panel=1,
				solved=data.getChallengeProgress(data.currentUserTeam,panel1.name,type),
				debugMode=debugMode,
				debug="N/A"
			)
		)
		response.set_cookie('Panel1DebugMode', debugMode)
		return response
	elif flask.request.method == 'POST':
		debugMode = request.cookies.get('Panel1DebugMode',"0")
		user = request.form["user"]
		pwd = request.form["pwd"]
		success, debug, message = panel1.panel1(user,pwd)
		if success:
			data.solveChallenge(data.currentUserTeam,panel1.name,type)
		return render_template("LoginPanels.html",
			panel=1,
			solved=data.getChallengeProgress(data.currentUserTeam,panel1.name,type),
			debugMode=debugMode,
			debug=debug,
			message=message
		)

# Panel 2: SQLi
data.enrollChallenge("loginPanels",panel2.name,"N/A",
{
    "1": "Irish names."
},
100,{
    "filter":{}
})

@loginpanels.route('/panel2',methods=['GET','POST'])
def viewPanel2():
	if flask.request.method == 'GET':
		debugMode = request.cookies.get('Panel2DebugMode',"0")
		response = make_response(
			render_template("LoginPanels.html",
				panel=2,
				solved=data.getChallengeProgress(data.currentUserTeam,panel2.name,type),
				debugMode=debugMode,
				debug="N/A"
			)
		)
		response.set_cookie('Panel2DebugMode', debugMode)
		return response
	elif flask.request.method == 'POST':
		debugMode = request.cookies.get('Panel2DebugMode',"0")
		user = request.form["user"]
		pwd = request.form["pwd"]
		success, debug, message = panel2.panel2(user,pwd)
		if success:
			data.solveChallenge(data.currentUserTeam,panel2.name,type)
		return render_template("LoginPanels.html",
			panel=2,
			solved=data.getChallengeProgress(data.currentUserTeam,panel2.name,type),
			debugMode=debugMode,
			debug=debug,
			message=message
		)
