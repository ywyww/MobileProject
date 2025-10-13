import datetime
from flask import Blueprint, jsonify, request

from app.db import models
from app.db.worker import SQLProviderRegulator

bp = Blueprint("regulators", __name__, url_prefix="/regulators")

@bp.route("/", methods=['GET', 'POST'])
def get_linked_regulators():
    if request.method == 'GET':
        """Get linked regulators"""
        regs = SQLProviderRegulator.get_linked_regulators()

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
            models.db.session.rollback()
            return f"{e}", 500


@bp.route("/mode", methods=['GET', 'POST'])
def get_modes():
    if request.method == 'GET':
        states = SQLProviderRegulator.get_regulator_modes()

        result = []
        for mode in states:
            result.append({
                'regulator_id': mode.regulator_id,
                'name': mode.name,
                'required': mode.required,
                'timestamp': mode.timestamp,
            })
        return jsonify(result)
    elif request.method == 'POST':
        try:
            json = request.get_json()
            
            regulator_id = int(json.get('regulator_id'))
            regulator = models.Regulator.query.get(regulator_id)
            if not regulator:
                raise Exception("Failed to find regulator")
            
            active_link = models.Link.query.filter_by(
                regulator_id=regulator_id, 
                status=True
            ).first()
            
            if not active_link:
                raise Exception("Regulator doesn't have active link")
            
            required_value = float(json.get('required'))
            
            new_mode = models.RegulationMode()
            new_mode.required=required_value
            new_mode.timestamp=datetime.datetime.now()
            new_mode.regulator_id=regulator_id
            
            models.db.session.add(new_mode)
            models.db.session.commit()
            
            return jsonify({
                'message': "Regulator mode inserted",
                'regulator_id': regulator_id,
                'regulator_name': regulator.name,
                'required': required_value,
                'timestamp': datetime.datetime.now().isoformat()
            }), 201
        
        except Exception as e:
            models.db.session.rollback()
            return f"{e}", 500
    ...