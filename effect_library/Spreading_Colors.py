import math
from array import array

buf = None
colors = [chex(_) for _ in '822d08', 'ec4b07', 'f9f697', 'fcd317', 'f7a72a']
# distance in pixels of each spot from the center of the string
dists = [0] * len(colors)
spotr = round(.04 * num_pixels)
span = .4
period = 60 * 4

def before_frame(frame):
    global buf
    buf = array('l', [-1] * num_pixels)
    f = math.sin((frame % period) / period * math.pi)
    nr = len(colors)
    for i in range(nr):
        dists[i] = round(num_pixels * f * span * (nr - i) / nr)
    for i in range(nr)[::-1]:
        for j in range(spotr):
            buf[dists[i] - j] = buf[dists[i] + j] = i

def render(index, frame):
    if buf[index] == -1:
        return black
    else:
        return chex(colors[buf[index]])
