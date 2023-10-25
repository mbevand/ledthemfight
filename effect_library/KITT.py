leader = 0
direction = 1
bins = 80
pixels = [0] * bins

def before_frame(frame):
    global leader, direction
    leader += direction
    if (leader >= bins):
        direction = -direction
        leader = bins - 1
    if (leader < 0):
        direction = -direction
        leader = 0
    pixels[leader] = 1
    for i in range(bins):
        pixels[i] *= .95

def render(index, frame):
    v = pixels[int(index * bins / num_pixels)]
    return rgb(v, 0, 0)
