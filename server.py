import flask
from flask import render_template,abort,redirect,request, make_response, g
import datetime
import os

from challenges import Crypto, Forensics, LFI, LoginPanels, Misc, OSINT, Stenography
from serverBackend import adminFunc, info, scorebot, data, auth

app = flask.Flask(__name__)
port = int(os.getenv('PORT', 8080))

app.register_blueprint(Crypto.crypto.crypto, url_prefix='/Challenges/Crypto')
app.register_blueprint(Forensics.forensics.forensics, url_prefix='/Challenges/Forensics')
app.register_blueprint(LFI.lfi.lfi, url_prefix='/Challenges/LFI')
app.register_blueprint(LoginPanels.loginpanels.loginpanels, url_prefix='/Challenges/LoginPanels')
app.register_blueprint(Misc.misc.misc, url_prefix='/Challenges')
app.register_blueprint(OSINT.osint.osint, url_prefix='/Challenges/OSINT')
app.register_blueprint(Stenography.stenography.stenography, url_prefix='/Challenges/Stenography')

app.register_blueprint(adminFunc.adminFunc, url_prefix='/adminPanel')
app.register_blueprint(info.info, url_prefix='/info')
app.register_blueprint(auth.auth, url_prefix='')
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.before_request
def authCheck():
	sessionToken = request.cookies.get('sessionToken')
	if (not sessionToken) or (not auth.JWTValidate(sessionToken)):
		if "Challenges" in request.path:
			return redirect("/login")
	return

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
