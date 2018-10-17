from socketIO_client import SocketIO, BaseNamespace

hostname = 'localhost'
port = 5000
command_namespace_path = '/commands'
room_name = 'dapost'


class CommandNamespace(BaseNamespace):

    __callback = None

    def set_listener(self, callback):
        self.__callback = callback

    def __parse_command(self, data):
        try:
            self.__callback(data)
        except TypeError as e:
            print(e)

    def on_event(self, event, *args):
        print(event)
        if event == 'command':
            try:
                self.__parse_command(args[0])
            except IndexError as e:
                print(e)


def test_callback(data):
    print("CALLBACK!__")
    print(data)


socketIO = SocketIO(hostname, port, CommandNamespace)
command_namespace = socketIO.define(CommandNamespace, command_namespace_path)
command_namespace.set_listener(test_callback)
command_namespace.emit('join', {'room': room_name})

socketIO.wait()
