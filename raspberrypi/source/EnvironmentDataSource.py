from .TemperatureData import TemperatureData
from .HumidityData import HumidityData
from .SoilMoistureData import SoilMoistureData


class EnvironmentDataSource:
    device = None
    mutex = None

    def __init__(self, device, mutex, observer):
        self.device = device
        self.mutex = mutex
        self.observer = observer

    def produce_data(self, data):
        if data[0:4] == "TEMP":
            self.observer.on_next(TemperatureData(data))
        elif data[0:4] == "HUMI":
            self.observer.on_next(HumidityData(data))
        elif data[0:3] == "SM0":
            self.observer.on_next(SoilMoistureData(data))


    def get_sensor_values(self):
        while True:
            self.mutex.acquire()
            try:
                val = self.device.readline().decode().strip('\r\n')
                if len(val) != 0:
                    print(val)

            except AttributeError:
                pass

            finally:
                self.mutex.release()
