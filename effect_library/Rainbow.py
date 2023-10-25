def render(index, frame):
    return hsv((2 * (index - int(frame / 2))) % num_pixels / num_pixels, 1, 1)
