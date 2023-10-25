spacing = max(4, round(num_pixels / 75))

def render(index, frame):
    return black if ((index + int(-frame / 5)) % spacing) else white
