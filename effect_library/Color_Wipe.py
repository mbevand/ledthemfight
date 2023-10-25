colors = (black, red, orange, yellow, lime, cyan, blue, magenta)
color_i = 0

def before_frame(frame):
    global color_i
    if not(frame % num_pixels):
        color_i += 1

def render(index, frame):
    i = color_i if index < (frame % num_pixels) else color_i - 1
    return colors[i % len(colors)]
