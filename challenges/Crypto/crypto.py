from flask import jsonify, send_file, Blueprint, render_template, abort, request
from serverBackend import data
import os
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
crypto = Blueprint('crypto',__name__,
    template_folder=template_folder,
    static_folder=static_folder)

data.enrollChallengeType("crypto")

@crypto.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
