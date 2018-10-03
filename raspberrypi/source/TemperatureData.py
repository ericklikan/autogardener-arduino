import datetime


class TemperatureData:
    value = 0
    timestamp = None

    def __init__(self, data, timestamp=datetime.datetime.now()):
        self.value = float(data[4:])
        self.timestamp = timestamp
