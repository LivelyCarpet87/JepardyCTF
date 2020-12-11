import jwt
from flask import render_template,abort,redirect,request, make_response, g, Blueprint
import datetime

from serverBackend import data

auth = Blueprint('auth', __name__,
						template_folder='./serverBackend/templates',
                        static_folder='./serverBackend/static')

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

def JWTGen(team,user):
    payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2, seconds=0),
			'iat': datetime.datetime.utcnow(),
			'team': team,
			'user': user,
		}
	jwtToken = jwt.encode(
			payload,
			data.jwtKey,
			algorithm='HS256'
		)
	return jwtToken

@auth.route('/login',methods=['GET','POST'])
def login():
    if flask.request.method == 'POST':
		user = request.form["user"]
		pwd = request.form["pwd"]

        team = None
        for teamName, teamData in teams:
            for user, userData in teamData["members"]:
                if userData["pass"] == pwd:
                    team = teamName

		if not success:
			return render_template("login.html",message="No such username and password pair created. Please sign up from the home page.")
		else:
			response = make_response( render_template("login.html",message="Logged in as member of Team "+team+".",redirect=True) )
            jwtToken = JWTGen(team,user)
			response.set_cookie('jwtToken', jwtToken)
			return response
	else:
		return render_template("login.html")

@auth.route("/register",methods=['GET','POST'])
def register():
	if flask.request.method == 'POST':
		registration = ""
		registration += request.form["user"]+":"
		registration += request.form["name"]+":"
		registration += request.form["wechatID"]+":"
		registration += request.form["password"]+"\n"
		f = open("./registration.txt", "a")
		f.write(registration)
		f.close()
		return "Your registration has been recieved. The admins will notify you once it is processed."
	return render_template("register.html")
