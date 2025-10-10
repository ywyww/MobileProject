import os

from flask import Flask
from sqlalchemy import create_engine
from .db import models
import datetime

def create_app(test_config=None):
    
    #app_dir = os.path.join(os.path.dirname(__file__))
    #db_path = os.path.join(app_dir, 'database.db')

    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    )
    
    models.db.init_app(app)
    
    with app.app_context():
        models.db.create_all()
        
        reg = models.Regulator()
        reg.name = "Test"

        sens = models.Sensor()
        sens.name = "Test2"

        models.db.session.add(reg)
        models.db.session.add(sens)
        models.db.session.flush()  

        link = models.Link()
        link.sensor_id = sens.id
        link.regulator_id = reg.id

        models.db.session.add(link)
        models.db.session.flush()  

        mode = models.RegulationMode()
        mode.regulator_id = reg.id
        mode.required = 320
        mode.timestamp = datetime.datetime.now()
        models.db.session.add(mode)

        models.db.session.commit()
        ...

    from .routers import regulators, sensors
    app.register_blueprint(regulators.bp)
    app.register_blueprint(sensors.bp)

    return app