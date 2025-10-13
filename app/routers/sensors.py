from flask import Blueprint, request, jsonify
from app.db.models import *

bp = Blueprint("sensors", __name__, url_prefix="/sensors")

@bp.route("/", methods=['GET', 'POST'])
def linked_sensors():
    if request.method == 'GET':
        """Get all sensors"""
        sensors = Sensor.query\
        .join(
            Link, Sensor.id == Link.sensor_id
        )\
        .where(Link.status == True)\
        .all()
        
        result = []
        for sensor in sensors:
            result.append({
                'id': sensor.id,
                'name': sensor.name,
            })
        return jsonify(result)
    elif request.method == 'POST':
        """Add and link sensor (opt w/out regulator)"""
        try:
            json = request.get_json()
            
            new_sensor = Sensor()
            new_sensor.name = json.get('name')
            
            db.session.add(new_sensor)
            db.session.flush()            

            new_link = Link()
            new_link.description = json.get('description')
            new_link.sensor_id = new_sensor.id
            new_link.regulator_id = json.get('regulator_id')
            db.session.add(new_link)

            db.session.commit()

            return jsonify({
                'message': 'Sensor created and linked successfully',
                'sensor_id': new_sensor.id,
                'sensor_name': new_sensor.name,
                'regulator_id': new_link.regulator_id
            }), 201
        except Exception as e:
            db.session.rollback()
            return f"{e}", 500


@bp.route("/measurements", methods=['GET'])
def sensors_measurements():
    """ Get sensor measurements """
    measurements = Measurement.query.all()

    result = []
    for measure in measurements:
        result.append({
            'id': measure.id,
            'name': measure.timestamp,
            'measurement': measure.measurement,
            'sensor_id': measure.sensor_id,
        })
    return jsonify(result)


@bp.route("/measurements/<int:i>", methods=['GET'])
def sensors_measurements_curr(i: int):
    """
    get current measurement
    """
    pass