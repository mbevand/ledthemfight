import math

# color spots, from the outer ones to the inner ones; note the outer ones
# will be rendered in the foreground and will eclipse the inner ones
colors = ('#822d08', '#ec4b07', '#f9f697', '#fcd317', '#f7a72a')
# distance in nr. of pixels between the center of the LED string and the
# outer boundary of the color spot
boundaries = [0] * len(colors)
# width of one half of the animation, relative to the length of the LED string
span = .5
# width in pixels of each color spot
spotw = round(span / len(colors) * num_pixels)
# nr. of frames during which the spots spread, or contract
period = 60 * 5

def before_frame(frame):
    # f goes from 0, to 1, back to 0, and so on, slowing down when reversing
    f = (math.sin((frame / period - .5) * math.pi) + 1) / 2
    nr = len(colors)
    for i in range(nr):
        boundaries[i] = round(num_pixels * f * span * (nr - i) / nr)

def render(index, frame):
    d = abs(index - num_pixels / 2)
    for i in range(len(colors)):
        if boundaries[i] >= d >= boundaries[i] - spotw:
            return colors[i]
    return black
