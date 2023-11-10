import math
from array import array

buf = None
colors = ('822d08', 'ec4b07', 'f9f697', 'fcd317', 'f7a72a')
# distance in pixels of each spot from the center of the string
dists = [0] * len(colors)
# radius in pixels of each color spot
spotr = round(.06 * num_pixels)
span = .45
period = 60 * 6

def before_frame(frame):
    global buf
    buf = array('l', [-1] * num_pixels)
    f = abs(math.cos((frame % (period * 2)) / period * math.pi) / 2 - .5)
    nr = len(colors)
    for i in range(nr):
        dists[i] = round(num_pixels * f * span * (nr - i - 1) / (nr - 1))
    center = round(num_pixels / 2)
    for i in range(nr)[::-1]:
        for j in range(spotr):
            for half in (-1, 1):
                for rhalf in (-1, 1):
                    buf_i = center + dists[i] * half + j * rhalf
                    if buf_i < len(buf):
                        buf[buf_i] = i

def render(index, frame):
    if buf[index] == -1:
        return black
    else:
        return chex(colors[buf[index]])
