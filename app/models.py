from sqlalchemy import *
from sqlalchemy.orm import *
from flask_sqlalchemy import *

class Base(DeclarativeBase, MappedAsDataclass):
    pass

db = SQLAlchemy(model_class=Base)

class Regulators(db.Model):
    __tablename__ = "regulators"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=True)
    ...


class States(db.Model):
    __tablename__ = "regulators_states"
   
    id = mapped_column(Integer, primary_key=True)
    state = mapped_column(Boolean, nullable=True)
    regulator_id = mapped_column(ForeignKey("regulators.id"))
    timestamp_id = mapped_column(ForeignKey("regulators_timestamps.id"))
    ...


class TimestampsRegulators(db.Model):
    __tablename__ = "regulators_timestamps"

    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(DateTime)
    ...


class Sensors(db.Model):
    __tablename__ = "sensors"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=True)
    ...


class Measurements(db.Model):
    __tablename__ = "sensors_measurements"
   
    id = mapped_column(Integer, primary_key=True)
    measurement = mapped_column(Float, nullable=True)
    sensor_id = mapped_column(ForeignKey("sensors.id"))
    timestamp_id = mapped_column(ForeignKey("sensors_timestamps.id"))
    ...


class TimestampsSensors(db.Model):
    __tablename__ = "sensors_timestamps"

    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(DateTime)
    ...
