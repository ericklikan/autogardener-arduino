from .source.EnvironmentDataSource import EnvironmentDataSource
from .controller import PlantController
from threading import Thread, Lock
import time

mutex = Lock()

controlDevice = PlantController('/dev/ttyUSB0', 9600, mutex)
data = EnvironmentDataSource(controlDevice.dev, mutex, observer)

t = Thread(target=data.get_sensor_values)
t.start()

time.sleep(20)
t2 = Thread(target=controlDevice.waterPlant())
t2.start()

time.sleep(20)
t2 = Thread(target=controlDevice.waterPlant(1))
t2.start()
