import datetime

from .Data import Data


class SoilMoistureData(Data):
    __sensor_index: int
    __value: int
    __timestamp: datetime.datetime

    def __init__(self, data, timestamp=datetime.datetime.now()):
        self.__sensor_index = int(data[3])
        self.__value = int(data[4:])
        self.__timestamp = timestamp

    @property
    def index(self):
        return self.__sensor_index

    @property
    def value(self):
        return self.__value

    @property
    def timestamp(self):
        return self.__timestamp
