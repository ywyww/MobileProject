from flask import Blueprint
from sqlalchemy import DateTime

bp = Blueprint("blueprint_set")

@bp.route("/regulators", ['GET'])
def regulators():
    pass

@bp.route("/regulators/{i}", ['GET'])
def regulators_curr(i: int):
    pass

@bp.route("/regulators/states", ['GET'])
def regulators():
    """
    get current state
    """
    pass

# measurements with date