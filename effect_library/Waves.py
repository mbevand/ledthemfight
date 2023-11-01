import math

colors = (blue, yellow)
segs = max(2, round(num_pixels / 30))
dist = None

def before_frame(frame):
    global dist
    dist = (1 + .9 * math.sin(math.pi * frame / 120)) / 2 * num_pixels / segs / 2

def render(index, frame):
    a = index % (num_pixels / segs)
    b = abs(a - num_pixels / segs / 2)
    return colors[0] if b < dist else colors[1]
