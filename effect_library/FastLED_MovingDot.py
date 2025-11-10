"""
MovingDot - Simple white dot moving along the strip
Translated from FastLED FirstLight example
The most basic animation - a foundation for learning
"""

# State
position = 0
direction = 1

def before_frame(frame):
    global position, direction
    
    # Move every 2 frames for visible speed
    if frame % 2 == 0:
        position += direction
        
        # Bounce at the ends
        if position >= num_pixels:
            position = num_pixels - 1
            direction = -1
        elif position < 0:
            position = 0
            direction = 1

def render(index, frame):
    if index == position:
        return white
    return black
