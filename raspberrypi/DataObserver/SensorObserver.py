from rx import Observer

from source.Data import Data
from .firebase import Firebase


class SensorObserver(Observer):

    def __init__(self):
        self.firebase = Firebase()

    def on_next(self, value: Data):
        self.firebase.update_data(str(value.type), value.value)

    def on_completed(self):
        return "Done"

    def on_error(self, error):
        return error
