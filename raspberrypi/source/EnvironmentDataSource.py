import serial
import time

class EnvironmentDataSource:
    device = None
    mutex = None

    def __init__(self, device, mutex):
        self.device = device
        self.mutex = mutex

    def get_sensor_values(self):
        while True:
            self.mutex.acquire()
            try:
                val = self.device.readline()
                if len(val) != 0:
                    print(val)
            finally:
                self.mutex.release()
