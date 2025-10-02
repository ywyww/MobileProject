from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import DateTime
from sqlalchemy import select, create_engine
from flask_sqlalchemy.session import Session
from app.db import models

bp = Blueprint("regulators", __name__, url_prefix="/regulators")

@bp.route("/", methods=['GET'])
def get_regulators():
    """Get all regulators"""
    regs = models.Regulators.query.all()
    
    result = []
    for regulator in regs:
        result.append({
            'id': regulator.id,
            'name': regulator.name,
        })
    
    return jsonify(result)


@bp.route("/states", methods=['GET', 'POST'])
def states():
    """
    get all state, push new state
    """
    pass


@bp.route("/states/<int:i>", methods=['POST'])
def push_state(i: int):
    """
    change sensor, change name, chane required value, change state
    """
    pass

# measurements with date