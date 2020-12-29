import flask
from flask import render_template,abort,redirect,request, make_response, g
from werkzeug.local import LocalProxy
import datetime
import os

from challenges import Crypto, Forensics, LFI, LoginPanels, Misc, OSINT, Stenography
from serverBackend import adminPanel, info, scorebot, data, auth

app = flask.Flask(__name__)
port = int(os.getenv('PORT', 8000))

app.register_blueprint(Crypto.crypto.crypto, url_prefix='/Challenges/Crypto')
app.register_blueprint(Forensics.forensics.forensics, url_prefix='/Challenges/Forensics')
app.register_blueprint(LFI.lfi.lfi, url_prefix='/Challenges/LFI')
app.register_blueprint(LoginPanels.loginpanels.loginpanels, url_prefix='/Challenges/LoginPanels')
app.register_blueprint(Misc.misc.misc, url_prefix='/Challenges')
app.register_blueprint(OSINT.osint.osint, url_prefix='/Challenges/OSINT')
app.register_blueprint(Stenography.stenography.stenography, url_prefix='/Challenges/Stenography')

app.register_blueprint(adminPanel.adminPanel, url_prefix='/adminPanel')
app.register_blueprint(info.info, url_prefix='/info')
app.register_blueprint(auth.auth, url_prefix='/')
app.config['TEMPLATES_AUTO_RELOAD'] = True

scorebot.init()


@app.before_request
def authCheck():
	if (auth.JWTValidate()==(None,None)):
		if "Challenges" in request.path:
			abort(403,"You are not logged in. Please visit /login to log in.")
	return

@app.after_request
def requestTmpClear(response):
	data.currentUser = None
	data.currentUserTeam = None
	return response

@app.route('/',methods=['GET','POST'])
def home():
	return render_template("home.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)
