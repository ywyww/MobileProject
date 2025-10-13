import wiringpi

from app.db.worker import SQLProviderRegulator


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
        regulators = SQLProviderRegulator.get_regulator_modes()
        
        for regulator in regulators:
            signal = self._calculate_regulator_signal(regulator.required, ...)   # PASTE SQL FOR PARSING SENSORS DATA
            wiringpi.pinMode(regulator.gpio, 1)       # Set pin 6 to 1 ( OUTPUT )
            wiringpi.digitalWrite(regulator.gpio, signal)
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
    