import flask
from flask import render_template,abort,redirect,request, make_response, g
import datetime
import os

from challenges import Crypto, Forensics, LFI, LoginPanels, Misc, OSINT, Stenography
from serverBackend import adminFunc, info, scorebot, data

app = flask.Flask(__name__)
port = int(os.getenv('PORT', 8080))

app.register_blueprint(Crypto.crypto.crypto, url_prefix='/Crypto')
app.register_blueprint(Forensics.forensics.forensics, url_prefix='/Forensics')
app.register_blueprint(LFI.lfi.lfi, url_prefix='/LFI')
app.register_blueprint(LoginPanels.loginpanels.loginpanels, url_prefix='/LoginPanels')
app.register_blueprint(Misc.misc.misc, url_prefix='/Misc')
app.register_blueprint(OSINT.osint.osint, url_prefix='/OSINT')
app.register_blueprint(Stenography.stenography.stenography, url_prefix='/Stenography')

app.register_blueprint(adminFunc.adminFunc, url_prefix='/adminPanel')
app.register_blueprint(info.info, url_prefix='/info')
app.config['TEMPLATES_AUTO_RELOAD'] = True


def JWTValidate(authToken):
	try:
		payload = jwt.decode(auth_token, data.jwtKey)
		g["team"] = payload["team"]
		g["user"] = payload["user"]
		return True
	except jwt.ExpiredSignatureError:
		return False
	except jwt.InvalidTokenError:
		return False

@app.before_request
def auth():
	sessionToken = request.cookies.get('sessionToken')
	if (not sessionToken) or (not JWTValidate(sessionToken)):
		return redirect("/login")
	return

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)