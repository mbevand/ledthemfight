"""
Lightning - Random lightning strikes effect
Creates dramatic flashes that illuminate the entire strip
"""

import random

# Lightning state
strike_active = False
strike_brightness = 0
strike_frame_start = 0
strike_duration = 0

def before_frame(frame):
    global strike_active, strike_brightness, strike_frame_start, strike_duration
    
    random.seed(frame)
    
    if not strike_active:
        # Random chance of lightning strike
        if random.random() < 0.01:  # 1% chance per frame
            strike_active = True
            strike_frame_start = frame
            strike_duration = random.randint(2, 8)  # 2-8 frames
            strike_brightness = random.uniform(0.7, 1.0)
    else:
        # Check if strike is over
        if frame - strike_frame_start >= strike_duration:
            strike_active = False
            strike_brightness = 0

def render(index, frame):
    if strike_active:
        # Full strip lights up during strike
        # Add some flicker
        random.seed(frame * 100 + index)
        flicker = random.uniform(0.8, 1.0)
        brightness = strike_brightness * flicker
        
        # White/blue lightning color
        return rgb(brightness, brightness, brightness * 1.1)
    
    # Dark stormy background with occasional purple glow
    random.seed(frame + index * 1000)
    if random.random() < 0.05:
        return rgb(0.05, 0, 0.1)  # Dim purple
    
    return rgb(0, 0, 0.01)  # Very dark blue
