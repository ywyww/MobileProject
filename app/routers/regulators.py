from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import DateTime
from sqlalchemy import select, create_engine
from flask_sqlalchemy.session import Session
from app.db import models

bp = Blueprint("regulators", __name__, url_prefix="/regulators")

@bp.route("/", methods=['GET', 'POST'])
def get_linked_regulators():
    if request.method == 'GET':
        """Get linked regulators"""
        regs = models.Regulator.query\
        .join(
            models.Link, models.Regulator.id == models.Link.regulator_id
        )\
        .where(models.Link.status == True)\
        .all()

        result = []
        for regulator in regs:
            result.append({
                'id': regulator.id,
                'name': regulator.name,
            })
        return jsonify(result)
    elif request.method == 'POST':
        """Set and link regulator"""
        try:
            json = request.get_json()

            new_regulator = models.Regulator()
            new_regulator.name = json.get('name')

            models.db.session.add(new_regulator)
            models.db.session.flush()

            sensor_id = json.get('sensor_id')

            sensor = models.Sensor.query.get(sensor_id)
            if not sensor:
                raise Exception("Failed to find sensor")

            new_link = models.Link()
            new_link.description = json.get('description')
            new_link.sensor_id=sensor_id
            new_link.regulator_id=new_regulator.id
            models.db.session.add(new_link)

            models.db.session.commit()

            return jsonify({
                'message': 'Regulator created and linked successfully',
                'regulator_id': new_regulator.id,
                'regulator_name': new_regulator.name
            }), 201
        except Exception as e:
            return f"{e}", 404


@bp.route("/mode", methods=['GET', 'POST'])
def get_modes():
    states = models.RegulationMode.query\
    .join(
        models.Regulator, models.RegulationMode.regulator_id == models.Regulator.id
    )\
    .join(
        models.Link, models.RegulationMode.regulator_id == models.Link.regulator_id
    )\
    .where(
        models.Link.status == True
    )\
    .add_columns(
        models.Link.regulator_id,
        models.Regulator.name,
        models.RegulationMode.required,
        models.RegulationMode.timestamp
    )\
    .all()

    result = []
    for mode in states:
        result.append(
        {
            'reg_id': mode.regulator_id,
            'name': mode.name,
            'required': mode.required,
            'timestamp': mode.timestamp,
        }
        )
    
    return jsonify(result)


@bp.route("/mode/<int:i>", methods=['POST'])
def push_state(i: int):
    """
    change name, change required value, change state
    """
    pass

# measurements with date