import multiprocessing
from threading import Lock
from rx import Observable
from rx.concurrency import ThreadPoolScheduler

from source.EnvironmentDataSource import EnvironmentDataSource
from source.controller import PlantController
from DataObserver.SensorObserver import SensorObserver

optimal_thread_count = multiprocessing.cpu_count()
scheduler = ThreadPoolScheduler(optimal_thread_count)

mutex = Lock()
observer = SensorObserver()
controlDevice = PlantController('/dev/ttyUSB0', 9600, mutex)
data = EnvironmentDataSource(controlDevice.dev, mutex)

Observable.create(data.get_sensor_values) \
        .subscribe_on(scheduler) \
        .subscribe(observer)

#
# Observable.interval(1000) \
#         .subscribe_on(scheduler) \
#         .subscribe(on_next=lambda i: controlDevice.waterPlant())
