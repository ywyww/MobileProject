from flask import Blueprint
from sqlalchemy import DateTime

bp = Blueprint("sensors", __name__, url_prefix="/sensors")

@bp.route("/", methods=['GET', 'POST'])
def sensors():
    pass

@bp.route("/<int:i>", methods=['GET', 'POST'])
def sensors_curr(i: int):
    """
    change name
    """
    pass

@bp.route("/measurements", methods=['GET'])
def sensors_measurements():
    """
    get current state
    """
    pass

# measurements with date