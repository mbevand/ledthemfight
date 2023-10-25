def render(index, frame):
    p = 120 
    frac = (frame % p) / p
    if frac <= .5:
        c = frac / .5
    else:
        c = (1 - (frac - .5) / .5)
    return rgb(0, 0, c)
