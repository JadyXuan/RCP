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
        GPIO.setup(self.pin_number, GPIO.OUT)

    def __call__(self, *args, **kwargs):
        result = self.get(*args, **kwargs)
        if result == True:
            GPIO.output(self.pin_number, GPIO.HIGH)
        elif result == False:
            GPIO.output(self.pin_number, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()

class GPIOReciever(object):
    def __init__(self, pin_number=None):
        GPIO.setmode(GPIO.BCM)
        if isinstance(pin_number, list):
            self.pin_number_list = pin_number.copy()
        elif isinstance(pin_number, (int, float)):
            self.pin_number_list = [pin_number]
        else:
            raise TypeError("Pin Number must be a number or list of numbers.")
        
        for pin in self.pin_number_list:
            GPIO.setup(pin, GPIO.IN)
        
        atexit.register(self.cleanup)
    
    def read(self):
        result_list = []
        for pin in self.pin_number_list:
            result_list.append(GPIO.input(pin))
        return result_list
    
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
        