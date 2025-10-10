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


class State(db.Model):
    __tablename__ = "state"
   
    id = mapped_column(Integer, primary_key=True)
    is_regulated = mapped_column(Boolean, nullable=True)    # reg value
    measurement = mapped_column(Float, nullable=True)   # sensor value
    timestamp = mapped_column(DateTime)
    link_id = mapped_column(ForeignKey("link.id"))
    ...
