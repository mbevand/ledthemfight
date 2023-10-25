def render(index, frame):
    n = max(1, num_pixels / 20)
    return white if int(index / n) % 2 else red
