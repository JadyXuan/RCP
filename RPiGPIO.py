import RPi.GPIO as GPIO
import time
import atexit

class GPIOSender(object):
    def __init__(self, getter):
        GPIO.setmode(GPIO.BCM)
        self.pin_number = 1
        self.get = getter
        atexit.register(self.cleanup)

    def set(self, **kwargs):
        self.__dict__.update(**kwargs)
        GPIO.setup(self.pin_number, GPIO.HIGH)

    def __call__(self, *args, **kwargs):
        result = self.get(*args, **kwargs)
        if result == True:
            GPIO.output(self.pin_number, GPIO.HIGH)
        elif result == False:
            GPIO.output(self.pin_number, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()


if __name__ == "__main__":
    @GPIOSender
    def getter():
        if hash(time.time()) % 2 == 0:  # 随机一下，懒得import randam
            return True
        else:
            return False
    
    getter.set(pin_number=14)
    while True:
        getter()
        time.sleep(5)
        