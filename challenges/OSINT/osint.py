from flask import jsonify, send_file, Blueprint, render_template, abort, request

import os
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
osint = Blueprint('osint', __name__,
                        template_folder=template_folder,
                        static_folder=static_folder)
@osint.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
