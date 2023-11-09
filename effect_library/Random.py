from random import random, seed

def render(index, frame):
    seed(int(frame / 10) * num_pixels + index)
    return hsv(random(), 1, 1)
