def render(index, frame):
    n = max(4, round(num_pixels / 20))
    colors = [purple_halloween] * n + [black] * 2 \
           + [orange_halloween] * n + [black] * 2 \
           ;
    return colors[(index + int(-frame / 4)) % len(colors)]
