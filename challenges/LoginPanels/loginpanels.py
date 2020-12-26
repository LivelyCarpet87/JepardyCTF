from flask import jsonify, send_file, Blueprint, render_template, abort, request, g

from . import panel0, panel1


import os
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
loginpanels = Blueprint('loginpanels', __name__,
						template_folder=template_folder,
						static_folder=static_folder)

@loginpanels.route('/',methods=['GET'])
def base():
	return render_template("listing.html")

@loginpanels.route('/panel0',methods=['GET','POST'])
def panel0():
	if flask.request.method == 'GET':
		debugMode = request.cookies.get('Panel0DebugMode',False)
		response = make_response(
			render_template("LoginPanels.html",
				panel=0,
				solved=data.teams["progress"].get("loginpanel0",False),
				debugMode=debugMode,
				debug="N/A"
			)
		)
		response.set_cookie('Panel0DebugMode', debugMode)
		return response
	elif flask.request.method == 'POST':
		debugMode = request.cookies.get('Panel0DebugMode',False)
		user = request.form["user"]
		pwd = request.form["pwd"]
		success, debug, message = panel0.panel0(user,pwd)
		if success:
			teamDataLock.acquire()
			data.teams["progress"]["loginpanel0"] = True
			teamDataLock.release()
		render_template("LoginPanels.html",
			panel=0,
			solved=data.teams["progress"].get("loginpanel0",False),
			debugMode=debugMode,
			debug=debug,
			message=message
		)

@loginpanels.route('/panel1',methods=['GET','POST'])
def panel1():
	if flask.request.method == 'GET':
		debugMode = request.cookies.get('Panel1DebugMode',False)
		response = make_response(
			render_template("LoginPanels.html",
				panel=1,
				solved=data.teams["progress"].get("loginpanel1",False),
				debugMode=debugMode,
				debug="N/A"
			)
		)
		response.set_cookie('Panel1DebugMode', debugMode)
		return response
	elif flask.request.method == 'POST':
		debugMode = request.cookies.get('Panel1DebugMode',False)
		user = request.form["user"]
		pwd = request.form["pwd"]
		success, debug, message = panel1.panel1(user,pwd)
		if success:
			teamDataLock.acquire()
			data.teams["progress"]["loginpanel1"] = True
			teamDataLock.release()
		render_template("LoginPanels.html",
			panel=1,
			solved=data.teams["progress"].get("loginpanel1",False),
			debugMode=debugMode,
			debug=debug,
			message=message
		)
