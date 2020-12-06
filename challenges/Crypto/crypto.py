from flask import jsonify, send_file, Blueprint, render_template, abort, request

crypto = Blueprint('crypto', __name__,
                        template_folder='./Crypto/templates')
@crypto.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
