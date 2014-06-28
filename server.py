import inspect

import web

r = None

class ErrorMessage(Exception):
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

def parseSpeed(speed_str):
    s = int(speed_str)
    if 0 > s > 500:
        raise ErrorMessage("0 < speed < 500", 400)
    return s

def parseDirection(dir_str):
    if direction in ("cw", "ccw"):
        return direction
    else:
        raise ErrorMessage("direction: 'cw' or 'ccw'", 400)

handlerMap = {
    "drive_straight": ("DriveStraight", {"speed": parseSpeed}),
    "stop": ("Stop", None),
    "dock": ("Dock", None),
    "turn_in_place": ("TurnInPlace", {"speed": parseSpeed,
                                      "direction": parseDirection}),
}

class Dispatcher(object):
    def handle(self, method, **kwargs):
        if method == "drive_straight":
            r.DriveStraight(parseSpeed(kwargs['speed']))
        elif method == "stop":
            r.Stop()
        elif method == "dock":
            r.Dock()
        elif method == "turn_in_place":
            r.TurnInPlace(parseSpeed(kwargs['speed']),
                          parseDirection(kwargs['direction']))
        else:
            print "unknown command: '%s'" % method

    def GET(self, method):
        print "GET:", web.input()
        self.handle(method, **web.input())

    def POST(self, method):
        print "POST:", web.input()
        self.handle(method, **web.input())

def register_routes(robot):
    global r
    r = robot
    return web.application(("/(.*)", "Dispatcher"),
                           {"Dispatcher": Dispatcher})

