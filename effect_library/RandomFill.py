import random

period = 120

def render(index, frame):
    # each pixel gets a specific seed for a given period
    random.seed(int(frame / period) * num_pixels + index)
    # the pixel will either fill or unfill at a specific frame in the period
    t = random.randint(0, period - 1)
    filling = not(int(frame / period) % 2)
    return yellow if ((frame % period) < t) ^ filling else blue
