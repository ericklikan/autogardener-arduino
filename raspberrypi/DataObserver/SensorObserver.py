from rx import Observer

from source.Data import Data


class SensorObserver(Observer):

    def on_next(self, value: Data):
        print(value.value)

    def on_completed(self):
        return "Done"

    def on_error(self, error):
        return error
