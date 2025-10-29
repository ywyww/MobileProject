import datetime
import logging
import atexit

from flask import Flask

from app.db import models
from app.backend.deviceManager import Model
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = None

def init_scheduler(app, model: Model):
    global scheduler
    
    scheduler = BackgroundScheduler()
    
    def use_regulators_with_context():
        with app.app_context():
            model.use_regulators()
    
    scheduler.add_job(
        func=use_regulators_with_context,
        trigger=IntervalTrigger(seconds=5),
        id='survey',
        name='опрос_датчиков',
        replace_existing=True
    )
    
    scheduler.start()
    logging.info("Scheduler started")
    
    atexit.register(shutdown_scheduler)

def shutdown_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown()
        logging.info("Scheduler stopped")

def create_app(test_config=None):
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        SCHEDULER_ENABLED=True,
        SENSORS_SURVEY_ENABLED=False
    )

    models.db.init_app(app)
    
    with app.app_context():
        models.db.create_all()
        
        reg = models.Regulator()
        reg.name = 'Test'
        reg.gpio = 8

        sens = models.Sensor()
        sens.name = 'Test2'
        sens.gpio = 10

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
        mode.required = 30
        mode.timestamp = datetime.datetime.now()
        
        models.db.session.add(mode)
        models.db.session.flush()

        models.db.session.commit()

    from .routers import regulators, sensors
    app.register_blueprint(regulators.bp)
    app.register_blueprint(sensors.bp)

    if app.config['SCHEDULER_ENABLED']:
        logging.debug('scheduler enabled')
        survey_flag = app.config['SENSORS_SURVEY_ENABLED']
        if survey_flag:
            logging.debug('sensors survey enabled')
        model = Model(survey_flag)
        init_scheduler(app, model)
    else:
        logging.debug('sensors survey mode disabled')

    return app
