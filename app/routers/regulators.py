from flask import Blueprint
from sqlalchemy import DateTime

bp = Blueprint("regulators", __name__, url_prefix="/regulators")

@bp.route("/", methods=['GET'])
def regulators():
    pass

@bp.route("/<int:i>", methods=['GET', 'POST'])
def regulators_curr(i: int):
    """
    change sensor, change name, chane required value, change state
    """
    pass

@bp.route("/states", methods=['GET'])
def states():
    """
    get current state
    """
    pass

# measurements with date