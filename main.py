import logging
import serial

import pyrobot
import server

class MockSerial(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def open(self):
        print "opening serial port: %s" % args

    def close(self):
        print "closing serial port"

    def write(self, inputdata):
        print "writing: %s" % repr(inputdata)

    def read(self, num_bytes):
        print "reading %d bytes" % num_bytes
        return " " * num_bytes

    def setDTR(self, state):
        print "set DTR: %s" % state


def main():
    sp = MockSerial()
    #sp = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

    robot = pyrobot.Roomba(sp)
    robot.sci.Wake()
    robot.Control() # TODO(tylerw): need to repeat if roomba sleeps?

    app = server.register_routes(robot)
    app.run()

if __name__ == "__main__":
    main()

