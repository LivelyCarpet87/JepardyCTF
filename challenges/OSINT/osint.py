from flask import jsonify, send_file, Blueprint, render_template, abort, request

osint = Blueprint('osint', __name__,
                        template_folder='./OSINT/templates')
@osint.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
