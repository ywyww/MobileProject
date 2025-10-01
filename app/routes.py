from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

bp.route("/get")
def get():
    pass

bp.route("/set")
def set():
    pass