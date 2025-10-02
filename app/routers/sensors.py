from flask import Blueprint
from sqlalchemy import DateTime

bp = Blueprint("blueprint_set")

@bp.route("/sensors", ['GET', 'POST'])
def sensors():
    pass

@bp.route("/sensors/{i}", ['GET', 'POST'])
def sensors_curr(i: int):
    pass

@bp.route("/sensors/measurements", ['GET'])
def sensors_measurements():
    """
    get current state
    """
    pass

# measurements with date