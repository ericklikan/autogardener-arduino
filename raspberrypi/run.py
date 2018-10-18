from threading import Thread, Lock

from source.EnvironmentDataSource import EnvironmentDataSource
from source.controller import PlantController
from DataObserver.SensorObserver import SensorObserver
from commands.command_parser import CommandParser

mutex = Lock()
observer = SensorObserver()
controlDevice = PlantController('/dev/ttyUSB0', 9600, mutex)
data = EnvironmentDataSource(controlDevice.dev, mutex)

observer_thread = Thread(target=data.get_sensor_values, args=[observer])
observer_thread.start()

commands = CommandParser()
commands.set_command_callback('WaterPlant', controlDevice.waterPlant)
