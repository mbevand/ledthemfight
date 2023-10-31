import random

state = {}
cols = (purple, orange_halloween)

def render(index, frame):
    ret = black
    if random.random() < 2 / num_pixels:
        state[index] = 1
    if index in state:
        f = state[index]
        c = cols[index % len(cols)]
        ret = rgb(f * c[0], f * c[1], f * c[2])
        state[index] *= .95 if state[index] > .3 else .7
        if state[index] < 1 / 255:
            del state[index]
    return ret
