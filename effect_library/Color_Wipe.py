colors = (black, red, orange, yellow, lime, cyan, blue, magenta)
color_i = 0
# the animation will move 1 pixel/frame for strings of length 0-60,
# 2 pixels/frame for 61-120, 3 pixels/frame for 121-180, etc
speed = 1 + int((num_pixels - 1) / 60)

def before_frame(frame):
    global color_i
    if not(frame % num_pixels):
        color_i += 1

def render(index, frame):
    i = color_i if index < ((frame * speed) % num_pixels) else color_i - 1
    return colors[i % len(colors)]
