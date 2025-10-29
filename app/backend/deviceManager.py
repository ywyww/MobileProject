import logging
import datetime
import OPi.GPIO as GPIO
import random as rand

from app.db.worker import SQLProviderRegulator
from app.db.models import *


class Model:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        ...


    def _calculate_regulator_signal(self, required_value, current_value) -> int:
        relay = Relay(required_value)
        return relay.update(current_value)

    def use_regulators(self):
        """
        Use last DB info for control regulators
        """
        logging.debug("Start using regulators")
        records = RegulationMode.query\
        .join(
            Regulator, RegulationMode.regulator_id == Regulator.id
        )\
        .join(
            Link, RegulationMode.regulator_id == Link.regulator_id
        )\
        .join(
            Sensor, Link.sensor_id == Sensor.id
        )\
        .where(
            Link.status == True
        )\
        .group_by(
            Link.regulator_id
        )\
        .order_by(
            func.max(RegulationMode.timestamp).desc()
        )\
        .add_columns(
            Sensor.id.label('sensor_id'),
            Sensor.name.label('sensor_name'),
            Sensor.gpio.label('sensor_gpio'),
            Regulator.id.label('regulator_id'),
            Regulator.name.label('regulator_name'),
            Regulator.gpio.label('regulator_gpio'),
            RegulationMode.required,
            RegulationMode.timestamp
        )\
        .all()
        
        ts = datetime.datetime.now()
        for record in records:
            try:
                # Сенсор - вход
                try:
                    GPIO.setup(record.sensor_gpio, GPIO.IN)
                except RuntimeError as e:
                    if "already configured" not in str(e):
                        raise
                
                #current = GPIO.input(record.sensor_gpio)
                current = rand.randint(25, 40)
                measure = Measurement()
                measure.measurement = current
                measure.sensor_id = record.sensor_id
                measure.timestamp = ts
                db.session.add(measure)

                signal = self._calculate_regulator_signal(record.required, current)
                logging.debug(f"signal {signal} to {record.sensor_gpio} from {record.regulator_gpio}")
                
                # Регулятор - выход
                try:
                    GPIO.setup(record.regulator_gpio, GPIO.OUT)
                except RuntimeError as e:
                    if "already configured" not in str(e):
                        raise
                
                GPIO.output(record.regulator_gpio, signal)

            except Exception as e:
                logging.error(f"Error processing GPIO {record.sensor_gpio}/{record.regulator_gpio}: {e}")
                continue

        db.session.commit()
        logging.debug("Stop using regulators")

class Relay:
    def __init__(self, required_value, bandcoeff=0.1):
        self.required_value = required_value
        self.band = required_value * bandcoeff
        self.raising = True
        ...

    def update(self, current_value: float) -> int:
        upper_bound = self.required_value + self.band / 2
        lower_bound = self.required_value - self.band / 2
        
        if current_value > upper_bound:
            self.raising = False
        elif current_value < lower_bound:
            self.raising = True
            
        if self.raising:
            return 1

        return 0
    ...
    
