from flask import jsonify, send_file, Blueprint, render_template, abort, request

misc = Blueprint('misc', __name__,
                        template_folder='./Misc/templates')
@misc.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
