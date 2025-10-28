# test_opi.py
import OPi.GPIO as GPIO
import time

def test_pin(mode_name, mode_value, pin):
    try:
        GPIO.setmode(mode_value)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)
        time.sleep(0.1)
        GPIO.output(pin, 0)
        GPIO.cleanup(pin)
        print(f"✓ {mode_name} пин {pin}: РАБОТАЕТ")
        return True
    except Exception as e:
        print(f"✗ {mode_name} пин {pin}: {e}")
        return False

# Тестируем разные режимы и пины
modes = [
    ("BOARD", GPIO.BOARD),
    ("BCM", GPIO.BCM), 
    ("SUNXI", GPIO.SUNXI)
]

pins_to_test = [
    # BOARD (физические)
    7, 8, 10, 11, 12, 13, 15, 16, 18,
    # BCM (номера GPIO)
    224, 225, 226, 227, 269, 270,
    # SUNXI (имена)
    "PA0", "PA1", "PA2", "PA3", "PA6", "PA7"
]

for mode_name, mode_value in modes:
    print(f"\n--- Тестируем режим {mode_name} ---")
    for pin in pins_to_test:
        test_pin(mode_name, mode_value, pin)
        time.sleep(0.1)
