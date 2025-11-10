"""
Plasma - Smooth plasma effect using sine waves
Creates organic, flowing color patterns
"""

import math

def render(index, frame):
    # Multiple sine waves at different frequencies create plasma effect
    x = index / num_pixels
    t = frame / 60.0
    
    # Layer multiple sine waves
    v1 = math.sin(x * 10 + t)
    v2 = math.sin(10 * (x * math.sin(t / 2) + t / 3))
    v3 = math.sin(x * 3 + t * 2)
    v4 = math.sin(math.sqrt((x - 0.5) ** 2) * 20 + t)
    
    # Combine waves
    plasma = (v1 + v2 + v3 + v4) / 4
    
    # Map to hue (full color spectrum)
    hue = (plasma + 1) / 2  # Normalize to 0-1
    
    return hsv(hue, 1, 1)
