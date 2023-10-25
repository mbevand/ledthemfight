def render(index, frame):
    p = 150
    return blue if frame % p < p / 2 else black
