def render(index, frame):
    if index < num_pixels / 3:
        return blue
    elif index < num_pixels * 2 / 3:
        return white
    else:
        return red
