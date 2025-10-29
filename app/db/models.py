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
    gpio = mapped_column(Integer, nullable=False)
    ...


class Sensor(db.Model):
    __tablename__ = "sensor"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=True)
    gpio = mapped_column(Integer, nullable=False)
    ...


class Link(db.Model):
    __tablename__ = "link"

    id = mapped_column(Integer, primary_key=True)
    description = mapped_column(String, nullable=True)
    status = mapped_column(Boolean, nullable=False, default=True)
    sensor_id = mapped_column(ForeignKey("sensor.id"), nullable=False)
    regulator_id = mapped_column(ForeignKey("regulator.id"), nullable=True)
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
    __tablename__ = "regulation_mode"
   
    id = mapped_column(Integer, primary_key=True)
    required = mapped_column(Float, nullable=True)
    timestamp = mapped_column(DateTime)
    regulator_id = mapped_column(ForeignKey("regulator.id"))
    ...  


class RegulationStatus(db.Model):
    """
    regulation status:
    regulator status (work or not) of installed regulator 
    @note RegulationMode
    """
    __tablename__ = "regulation_status"

    id = mapped_column(Integer, primary_key=True)
    worked = mapped_column(Boolean, nullable=False)
    timestamp = mapped_column(DateTime)
    regulation_mode_id = mapped_column(ForeignKey("regulation_mode.id"))
    ...