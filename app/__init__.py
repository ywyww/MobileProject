import os

from flask import Flask
from sqlalchemy import create_engine
from .db import models

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
        
        reg = models.Regulators()
        reg.name = "Test"
        models.db.session.add(reg)
        models.db.session.commit()
        ...

    from .routers import regulators, sensors
    app.register_blueprint(regulators.bp)
    app.register_blueprint(sensors.bp)

    return app