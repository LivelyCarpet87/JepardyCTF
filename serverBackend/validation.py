from flask import jsonify, send_file, Blueprint, render_template, abort, request, g
login = Blueprint('login', __name__,template_folder='./serverBackend/templates')

@login.route('',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return render_template("login.html")
    elif flask.request.method == 'POST':
        user = request.form["user"]
		pwd = request.form["pwd"]
