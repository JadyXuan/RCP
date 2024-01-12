import RPi.GPIO as GPIO
import time
import atexit

class GPIOSender(object):
    def __init__(self, getter):
        GPIO.setmode(GPIO.BCM)
        self.pin_number = None
        self.get = getter
        atexit.register(self.cleanup)

    def set(self, **kwargs):
        self.__dict__.update(**kwargs)
        
        if self.pin_number is None:
            raise TypeError("Pin Number should not be None.")
        elif isinstance(self.pin_number, (int, float)):
            self.pin_number = [self.pin_number]
        elif isinstance(self.pin_number, list):
            self.pin_number = self.pin_number.copy()
        else:
            raise TypeError("Pin Number must be a number or list of numbers.")
        
        for pin in self.pin_number:
            GPIO.setup(pin, GPIO.OUT)
            print("Set GPIO{} as output pin.".format(self.pin_number))

    def __call__(self, *args, **kwargs):
        result = self.get(*args, **kwargs)
        if isinstance(result, bool):
            result_list = [result]
        elif isinstance(result, list):
            result_list = result.copy()
        else:
            raise TypeError("Sender message must be a bool or list of bools.")
        for i, pin in enumerate(self.pin_number):
            GPIO.output(pin, GPIO.HIGH) if result_list[i] else GPIO.output(pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()

class GPIOReciever(object):
    def __init__(self, pin_number=None, mode="in"):
        GPIO.setmode(GPIO.BCM)
        self.mode_list = []
        if isinstance(pin_number, list):
            self.pin_number_list = pin_number.copy()
        elif isinstance(pin_number, (int, float)):
            self.pin_number_list = [pin_number]
        else:
            raise TypeError("Pin Number must be a number or list of numbers.")
        
        if isinstance(mode, str):
            for i in range(len(self.pin_number_list)):
                self.mode_list.append(mode)
        elif isinstance(mode, list):
            self.mode_list = mode.copy()
        else:
            raise TypeError("Mode must be a str or list of strs.")

        for i, pin in enumerate(self.pin_number_list):
            if self.mode_list[i] == "in":
                GPIO.setup(pin, GPIO.IN)
                print("Set GPIO{} as input pin".format(pin))
            elif self.mode_list[i] == "out":
                GPIO.setup(pin, GPIO.OUT)
                print("Set GPIO{} as input pin".format(pin))
        
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
        