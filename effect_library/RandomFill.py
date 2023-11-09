import random

period = 120 # nr. of frames during which the string either fills or unfills
hold = 10 # nr. of frames at beginning/end of period when nothing happens

def render(index, frame):
    # each pixel gets a specific seed for a given period
    random.seed(int(frame / period) * num_pixels + index)
    # the pixel will either fill or unfill at a specific frame in the period
    t = random.randint(1 + hold, period - 1 - hold)
    filling = not(int(frame / period) % 2)
    return yellow if ((frame % period) < t) ^ filling else blue
