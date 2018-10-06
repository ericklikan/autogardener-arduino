from rx import Observer
from serial import Serial
from threading import Lock

from time import sleep

from .TemperatureData import TemperatureData
from .HumidityData import HumidityData
from .SoilMoistureData import SoilMoistureData


class EnvironmentDataSource:
    __device: Serial
    __mutex: Lock
    __observer: Observer

    def __init__(self, device: Serial, mutex: Lock):
        self.__device = device
        self.__mutex = mutex

    def produce_data(self, data, observer: Observer):
        if data[0:4] == "TEMP":
            observer.on_next(TemperatureData(data))
        elif data[0:4] == "HUMI":
            observer.on_next(HumidityData(data))
        elif data[0:3] == "SM0":
            observer.on_next(SoilMoistureData(data))

    def get_sensor_values(self, observer: Observer):
        while True:
            self.__mutex.acquire()
            try:
                val = self.__device.readline().decode().strip('\r\n')
                if len(val) != 0:
                    self.produce_data(val, observer)

            except (ValueError, ValueError, UnicodeDecodeError) as e:
                print(e)
                self.__device.dtr = True
                sleep(1)

                self.__device.flushInput()
                self.__device.dtr = False

            finally:
                self.__mutex.release()



