"""
TwinkleStars - Random twinkling stars effect
Inspired by FastLED TwinkleFox example
Stars randomly fade in and out across the strip
"""

import random
import math

# Star data: {index: {'brightness': value, 'phase': value, 'speed': value}}
stars = {}
MAX_STARS = None  # Will be set based on num_pixels

def before_frame(frame):
    global stars, MAX_STARS
    
    if MAX_STARS is None:
        MAX_STARS = max(5, num_pixels // 4)
    
    # Update existing stars
    for idx in list(stars.keys()):
        star = stars[idx]
        star['phase'] += star['speed']
        
        # Calculate brightness using sine wave for smooth fade in/out
        star['brightness'] = (math.sin(star['phase']) + 1) / 2
        
        # Remove star if cycle complete
        if star['phase'] >= math.pi * 2:
            del stars[idx]
    
    # Add new stars randomly
    random.seed(frame)
    if len(stars) < MAX_STARS and random.random() < 0.1:
        new_idx = random.randint(0, num_pixels - 1)
        if new_idx not in stars:
            stars[new_idx] = {
                'brightness': 0,
                'phase': 0,
                'speed': random.uniform(0.02, 0.08),  # Random twinkle speed
                'hue': random.random()  # Random color
            }

def render(index, frame):
    if index in stars:
        star = stars[index]
        # Twinkling stars with varying colors
        return hsv(star['hue'], 0.7, star['brightness'])
    
    # Background: very dim blue
    return rgb(0, 0, 0.02)
