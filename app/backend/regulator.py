import logging

# TODO добавить использование OPi GPIO и инициализацию через бдшку

class Model:
    def __init__(self):
        self.regulators: dict[int][Relay] = {}
    
    def add_regulator(self, GPIO, required_value, state=False, bandcoeff=0.1):
        if (GPIO in self.regulators.keys()):
            logging.debug(f"Regulator on {GPIO} replaced/disabled/has changed required_value")
        self.regulators[GPIO] = Relay(GPIO, required_value, state, bandcoeff)

    def calculate_regulator_signal(self, GPIO, current_value) -> int:
        regulator: Relay = self.regulators[GPIO]
        if (regulator):
            return regulator.update(current_value)
        return 0
    
    def use_regulators(self):
        ...
    ...

class Relay:
    def __init__(self, GPIO, required_value, state=False, bandcoeff=0.1):
        self.pin = GPIO
        self.required_value = required_value
        self.state = state
        self.band = required_value * bandcoeff
        self.raising = True
        ...

    def update(self, current_value: float) -> int:
        if (self.state):
            upper_bound = self.required_value + self.band / 2
            lower_bound = self.required_value - self.band / 2
            control_signal = 0
            
            if current_value > upper_bound:
                self.raising = False
            elif current_value < lower_bound:
                self.raising = True
                
            if self.raising:
                control_signal = 1
            else:
                control_signal = -1

            return control_signal
        return 0
    
    ...
    