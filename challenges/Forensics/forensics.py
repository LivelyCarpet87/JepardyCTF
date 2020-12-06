from flask import jsonify, send_file, Blueprint, render_template, abort, request

forensics = Blueprint('forensics', __name__,
                        template_folder='./Forensics/templates')
@forensics.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
