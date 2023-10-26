import random

nose = '_' * int(num_pixels / 80)
eyes = ['oo_' + nose + '_oo', # eyes opened
        '_o_' + nose + '_o_'] # eyes closed
pos = None                              # position of the eyes
age = 0         # age of eyes (in nr. of frames since creation)
life = 250      # duration (in nr. of frames) that the eyes are lit up
closedperiod = range(130,135)
fade = 50       # duration (in nr. of frames) of the fade-in and fade-out

def before_frame(frame):
    global pos, age
    if pos is None:
        pos = round((num_pixels - len(eyes[0])) * random.random())
        age = -1
    age += 1
    if age > life:
        pos = None

def fade_in_out(color):
    k = 1
    if age < fade:
        denom = age # fade in
    elif age >= life - fade:
        denom = life - age # fade out
    else:
        return color
    k = fade / denom if denom else fade * 2
    return dim(color, k)

def render(index, frame):
    if pos is None:
        return black
    i = index - pos
    openclose = 0 if age not in closedperiod else 1
    if i >= 0 and i < len(eyes[openclose]) and eyes[openclose][i] == 'o':
        return fade_in_out(red)
    else:
        return black
