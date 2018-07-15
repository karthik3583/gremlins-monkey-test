import os


class Ind:
    event = None
    input = None
    locx = None
    locy = None
    duration = None
    distancex = None
    distancey = None
    scale = None
    rotation = None
    radius = None
    dom = None

    def __init__(self, _e, _i=None, _lx=None, _ly=None, _du=None, _dx=None, _dy=None,
                 _scale=None, _rotation=None, _radius=None,
                 _dom=None):
        self.event = _e
        self.input = _i
        self.locx = _lx
        self.locy = _ly
        self.duration = _du
        self.distancex = _dx
        self.distancey = _dy
        self.scale = _scale
        self.rotation = _rotation
        self.radius = _radius
        self.dom = _dom

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            self.event, self.input, self.locx, self.locy,
            self.duration, self.distancex, self.distancey,
            self.scale, self.rotation, self.radius,
            self.dom
        )



def read_log(path):
    if not os.path.exists(path):
        return None

    events = set()
    atomic_sequences = []

    with open(path, "r") as f:
        lines = f.readlines()
        for l in lines:
            if l.find("VM26 gremlinsClient.js:") == -1:
                continue
            parts = l.split()
            if parts[2] == "gremlin":
                # print(parts[5:])
                events.add(parts[4])
                e = parts[4]
                o = None
                if e == "type":
                    o = Ind(_e=e, _i=parts[5], _lx=parts[7], _ly=parts[8])
                elif e == "click" or e == "scroll"\
                        or e == "mousedown" or e == "mouseout"\
                        or e == "mouseover" or e == "dblclick"\
                        or e == "mousemove" or e == "mouseup":
                    o = Ind(_e=e, _lx=parts[6], _ly=parts[7])
                elif e == "gesture":
                    o = Ind(_e=e, _lx=parts[6], _ly=parts[7], _dx=int(parts[9].replace(",", "")),
                            _dy=int(parts[11].replace(",", "")),
                            _du=int(parts[13].replace("}", "")))
                elif e == "tap" or e == "doubletap":
                    o = Ind(_e=e, _lx=parts[6], _ly=parts[7], _du=int(parts[9].replace("}", "")))
                elif e == "multitouch":
                    o = Ind(_e=e, _lx=parts[6], _ly=parts[7], _dx=int(parts[15].replace(",", "")),
                            _dy=int(parts[17].replace(",", "")),
                            _scale=float(parts[9].replace(",", "")),
                            _rotation=int(parts[11].replace(",", "")),
                            _radius=int(parts[13].replace(",", ""))
                            )
                elif e == "input":
                    o = Ind(_e=e, _i=parts[5], _dom=''.join(str(e) for e in parts[7:]))

                if o is not None:
                    print(o)
                    atomic_sequences.append(o)



read_log("gremlins.log")
