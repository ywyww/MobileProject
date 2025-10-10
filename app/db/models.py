from sqlalchemy import *
from sqlalchemy.orm import *
from flask_sqlalchemy import *

class Base(DeclarativeBase, MappedAsDataclass):
    pass

db = SQLAlchemy(model_class=Base)

class Regulator(db.Model):
    __tablename__ = "regulator"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=True)
    ...

class Sensor(db.Model):
    __tablename__ = "sensor"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=True)
    ...


class Link(db.Model):
    __tablename__ = "link"
    id = mapped_column(Integer, primary_key=True)
    sensor_id = mapped_column(ForeignKey("sensor.id"))
    regulator_id = mapped_column(ForeignKey("regulator.id"))
    ...


class Measurement(db.Model):
    __tablename__ = "sensor_measurement"
    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(DateTime)
    measurement = mapped_column(Float)
    sensor_id = mapped_column(ForeignKey("sensor.id"))
    ...


class RegulationMode(db.Model):
    """
    regulation mode:
    if regulator is working: required value has been setted 
    else required value is null or this table dont care
    """
    __tablename__ = "regulation_state"
   
    id = mapped_column(Integer, primary_key=True)
    required = mapped_column(Float, nullable=True)
    timestamp = mapped_column(DateTime)
    regulator_id = mapped_column(ForeignKey("regulator.id"))
    ...  
