from flask import jsonify, send_file, Blueprint, render_template, abort, request

stenography = Blueprint('stenography', __name__,
                        template_folder='./Stenography/templates')
@stenography.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
