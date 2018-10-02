import time

import serial


class PlantController:

    def __init__(self, device, baud_rate, mutex):
        try:
            self.dev = serial.Serial(device, baud_rate, timeout=0)
            print('Initialized Serial Device.')
            self.success = True
            self.mutex = mutex
            self.clear_buffer()

        except:
            print('Error: Something went wrong.')
            self.success = False

    def clear_buffer(self):
        while True:
            res = self.dev.readline()
            if res == b'':
                break
        self.dev.flush()

    def __send_command(self, command, params=()):
        self.mutex.acquire()
        writebuffer = []
        if len(params) > 0:
            writebuffer.append(len(params) + 1)

        writebuffer.append(command)

        if len(params) > 0:
            writebuffer += params

        for item in writebuffer:
            self.dev.write('{}\n'.format(item).encode())
        ret = []

        while True:
            res = self.dev.readline()
            if res not in [b'busy\r\n', b'done\r\n']:
                ret.append(res.decode().strip('\r\n'))
            if res == b'done\r\n':
                break
        self.dev.flush()
        self.mutex.release()
        return ret

    def waterPlant(self, seconds=-1):
        print("watering")
        if seconds == -1:
            self.__send_command('WATER')
        else:
            self.__send_command('WATER', [seconds])

