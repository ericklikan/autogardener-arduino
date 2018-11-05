from socketIO_client import SocketIO, BaseNamespace
from threading import Thread
from DataObserver.store.store import retrieve

hostname = 'auto-garden.herokuapp.com'
port = None
command_namespace_path = '/commands'
room_name = retrieve("userid")


class CommandNamespace(BaseNamespace):

    __callback = None

    def set_listener(self, callback):
        self.__callback = callback

    def __parse_command(self, data):
        try:
            self.__callback(data['command'], data['data'])
        except (TypeError, KeyError) as e:
            print(e)

    def on_event(self, event, *args):
        if event == 'command':
            try:
                self.__parse_command(args[0])
            except IndexError as e:
                print(e)


class CommandParser:

    __callbacks = {}

    def __init__(self):
        self.__path = command_namespace_path
        self.__port = port
        self.__room = room_name
        self.__hostname = hostname
        self.__socket = SocketIO(self.__hostname, self.__port, CommandNamespace)
        self.__namespace = self.__socket.define(CommandNamespace, self.__path)
        self.__namespace.set_listener(self.listener)
        self.__namespace.emit('join', {'room': room_name})
        t = Thread(target=self.__socket.wait)
        t.start()

    def set_command_callback(self, command, command_callback):
        self.__callbacks[command] = command_callback

    def delete_command_callback(self, command):
        del self.__callbacks[command]

    def listener(self, command, data):
        try:
            self.__callbacks[command](data)
        except KeyError as e:
            print(e)
