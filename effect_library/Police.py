def render(index, frame):
    step = int(frame / 2)
    pattern = 'f_____f_____f___'
    pi = step % len(pattern)
    if pattern[pi] == 'f':
        if int(step / len(pattern)) % 2:
            if index < num_pixels / 2:
                return blue
        else:
            if index >= num_pixels / 2:
                return red
    return black
