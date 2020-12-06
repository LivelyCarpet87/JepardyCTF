from flask import jsonify, send_file, Blueprint, render_template, abort, request

lfi = Blueprint('lfi', __name__,
                        template_folder='./LFI/templates')
@lfi.route('/',methods=['GET'])
def base():
    return render_template("listing.html")
