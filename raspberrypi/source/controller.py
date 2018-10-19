from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from time import sleep


class PlantController:

    def __init__(self, device, baud_rate, mutex):
        try:
            self.dev = Serial(device,
                              baud_rate,
                              bytesize=EIGHTBITS,
                              parity=PARITY_NONE,
                              stopbits=STOPBITS_ONE,
                              timeout=0,
                              xonxoff=0,
                              rtscts=0)
            print('Initialized Serial Device.')
            self.success = True
            self.mutex = mutex
            self.dev.dtr = True
            sleep(1)
            self.dev.flushInput()
            self.dev.dtr = False

        except Exception as e:
            print(e)
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
        ret = []

        try:
            writebuffer = []
            if len(params) > 0:
                writebuffer.append(len(params) + 1)

            writebuffer.append(command)

            if len(params) > 0:
                writebuffer += params

            for item in writebuffer:
                self.dev.write('{}\n'.format(item).encode())

            while True:
                res = self.dev.readline()
                # if res not in [b'busy\r\n', b'done\r\n']:
                #     ret.append(res.decode().strip('\r\n'))
                if res == b'done\r\n':
                    break
            self.dev.flush()

        except (ValueError, ValueError, UnicodeDecodeError) as e:
            print(e)
            self.dev.dtr = True
            sleep(1)

            self.dev.flushInput()
            self.dev.dtr = False

        self.mutex.release()

        return ret

    def waterPlant(self, seconds=-1):
        if seconds == -1:
            self.__send_command('WATER')
        else:
            self.__send_command('STWAT')
            sleep(seconds)
            self.__send_command('SPWAT')

