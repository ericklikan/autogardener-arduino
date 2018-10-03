import datetime


class SoilMoistureData:
    sensor_index = None
    value = 0
    timestamp = None

    def __init__(self, data, timestamp=datetime.datetime.now()):
        self.value = int(data[3])
        self.value = int(data[4:])
        self.timestamp = timestamp
