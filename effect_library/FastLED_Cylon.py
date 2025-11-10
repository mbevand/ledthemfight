"""
Cylon - Larson Scanner effect
Translated from FastLED example
A single bright LED moves back and forth with a fading trail
All LEDs cycle through the rainbow colors
"""

# State
position = 0
direction = 1
fade_buffer = {}

def before_frame(frame):
    global position, direction
    
    # Move the position
    position += direction
    
    # Bounce at the ends
    if position >= num_pixels:
        position = num_pixels - 1
        direction = -1
    elif position < 0:
        position = 0
        direction = 1
    
    # Fade all pixels
    for i in range(num_pixels):
        if i in fade_buffer:
            fade_buffer[i] *= 0.98  # nscale8(250) ≈ 250/255
            if fade_buffer[i] < 0.01:
                del fade_buffer[i]

def render(index, frame):
    # Calculate hue that continuously cycles
    hue = (frame / 2) % 360  # Changes every 2 frames
    
    if index == position:
        # Set the current position to full brightness
        fade_buffer[index] = 1.0
        return hsv((hue + index) / 360, 1, 1)
    elif index in fade_buffer:
        # Return faded color
        return hsv((hue + index) / 360, 1, fade_buffer[index])
    
    return black
