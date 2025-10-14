import wiringpi

from app.db.worker import SQLProviderRegulator
from app.db.models import *


class Model:
    def __init__(self):
        wiringpi.wiringPiSetup()
        ...


    def _calculate_regulator_signal(self, required_value, current_value) -> int:
        relay = Relay(required_value)
        return relay.update(current_value)


    def use_regulators(self):
        """
        Use last DB info for control regulators
        """
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
        
        for record in records:
            wiringpi.pinMode(record.sensor_gpio, 0)
            current = wiringpi.digitalRead(record.sensor_gpio)
            signal = self._calculate_regulator_signal(record.required, current)
            wiringpi.pinMode(record.regulator_gpio, 1)
            wiringpi.digitalWrite(record.regulator_gpio, signal)
        ...
    ...


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
    