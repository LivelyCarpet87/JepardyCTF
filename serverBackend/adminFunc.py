from flask import jsonify, send_file, Blueprint, render_template, abort, request, g
adminFunc = Blueprint('adminFunc', __name__)
