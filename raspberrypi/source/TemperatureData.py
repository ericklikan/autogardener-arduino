import datetime

from .Data import Data


class TemperatureData(Data):
    __type = "Temperature"
    __value: float
    __timestamp: datetime.datetime

    def __init__(self, data, timestamp=datetime.datetime.now()):
        self.__value = float(data[4:])
        self.__timestamp = timestamp

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @property
    def timestamp(self):
        return self.__timestamp
