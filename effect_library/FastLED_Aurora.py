"""
Aurora - Northern lights effect
Slow, ethereal waves of green and purple
"""

import math

def render(index, frame):
    # Multiple slow sine waves create aurora effect
    t = frame / 60.0
    x = index / num_pixels
    
    # Base wave (primary green)
    wave1 = math.sin(x * 3 + t * 0.5) * 0.5 + 0.5
    wave2 = math.sin(x * 5 - t * 0.3 + 2) * 0.5 + 0.5
    wave3 = math.sin(x * 2 + t * 0.7 + 4) * 0.5 + 0.5
    
    # Combine waves
    green_intensity = (wave1 * 0.5 + wave2 * 0.3 + wave3 * 0.2)
    
    # Add purple undertones
    purple_wave = math.sin(x * 4 + t * 0.4 + 1) * 0.5 + 0.5
    purple_intensity = purple_wave * 0.3
    
    # Create aurora colors
    r = purple_intensity * 0.5
    g = green_intensity * 0.8
    b = (green_intensity * 0.3 + purple_intensity * 0.7)
    
    # Add some sparkle
    import random
    random.seed(frame * 1000 + index)
    if random.random() < 0.02:
        sparkle = random.uniform(0.3, 0.6)
        r += sparkle
        g += sparkle
        b += sparkle
    
    return rgb(min(1, r), min(1, g), min(1, b))
