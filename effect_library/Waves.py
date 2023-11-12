import math

colors = (cyan, blue)
segs = max(2, round(num_pixels / 30))
period = 100 # period of oscillations (in nr. of frames)
dist = None

def before_frame(frame):
    def s(x):
        # the s() function flattens the sine wave so that the oscillation
        # of waves slows down more significantly before reversing direction;
        # f=1 does not alter the sine wave, and the closer it is to 0 the
        # flatter the sine wave is
        f = .8
        return x**f if x >= 0 else -abs(x)**f
    global dist
    dist = (1 + .9 * s(math.sin(math.pi * frame / period))) / 2 * \
        num_pixels / segs / 2

def render(index, frame):
    d = abs(index % (num_pixels / segs) - num_pixels / segs / 2)
    return colors[0] if d < dist else colors[1]
