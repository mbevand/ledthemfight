from random import randint, seed

period = 120 # nr. of frames that each pixel blinks one color then the other
every = 3 # only light up 1 out of <every> pixel

def render(index, frame):
    # each pixel's blinking phase is offset by a random number of frames
    seed(index)
    f = (frame + randint(0, period - 1)) % period
    return black if index % every > 0 else green if f < period / 2 else red
