clen = max(10, int(num_pixels / 15))

def render(index, frame):
    intens = ((index + int(-frame / 5)) % clen + 1) / clen
    intens *= intens
    return mul(lime, intens)
