from threading import Thread, Lock

from source.EnvironmentDataSource import EnvironmentDataSource
from source.controller import PlantController
from DataObserver.SensorObserver import SensorObserver

mutex = Lock()
observer = SensorObserver()
controlDevice = PlantController('/dev/ttyUSB0', 9600, mutex)
data = EnvironmentDataSource(controlDevice.dev, mutex)

t = Thread(target=data.get_sensor_values(observer))
t.start()

#
# Observable.interval(1000) \
#         .subscribe_on(scheduler) \
#         .subscribe(on_next=lambda i: controlDevice.waterPlant())
