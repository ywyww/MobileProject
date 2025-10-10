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
    description = mapped_column(String, nullable=True)
    ...

class Measurement(db.Model):
    __tablename__ = "sensor_measurement"
    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(DateTime)
    measurement = mapped_column(Float)
    ...

class SensorState(db.Model):
    __tablename__ = "sensor_state"
   
    id = mapped_column(Integer, primary_key=True)
    state = mapped_column(Boolean, nullable=False)
    timestamp = mapped_column(DateTime)
    sensor_id = mapped_column(ForeignKey("sensor.id"))
    ...


class RegulatorState(db.Model):
    __tablename__ = "regulator_state"
   
    id = mapped_column(Integer, primary_key=True)
    state = mapped_column(Boolean, nullable=False)
    timestamp = mapped_column(DateTime)
    regulator_id = mapped_column(ForeignKey("regulator.id"))
    ...  
