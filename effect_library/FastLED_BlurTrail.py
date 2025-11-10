"""
BlurTrail - Moving dot with blur effect
Translated from FastLED Blur example by Zach Vorhies
A bright pixel moves along the strip with a beautiful blur trail
"""

# State
pos = 0
direction = 1
brightness_buffer = {}

def before_frame(frame):
    global pos, direction
    
    # Move position every other frame for smooth motion
    if frame % 2 == 0:
        pos += direction
        
        # Bounce at ends
        if pos >= num_pixels:
            pos = num_pixels - 1
            direction = -1
        elif pos < 0:
            pos = 0
            direction = 1
    
    # Apply blur and fade to all pixels
    new_buffer = {}
    for i in range(num_pixels):
        if i in brightness_buffer:
            # Blur by averaging with neighbors
            left = brightness_buffer.get(i - 1, 0) if i > 0 else 0
            right = brightness_buffer.get(i + 1, 0) if i < num_pixels - 1 else 0
            center = brightness_buffer[i]
            
            # Weighted average for blur (center gets more weight)
            blurred = (left * 0.2 + center * 0.6 + right * 0.2)
            
            # Fade to black
            blurred *= 0.94  # fadeToBlackBy(16/255)
            
            if blurred > 0.01:
                new_buffer[i] = blurred
    
    brightness_buffer.clear()
    brightness_buffer.update(new_buffer)
    
    # Add the bright moving dot
    brightness_buffer[pos] = 1.0

def render(index, frame):
    if index in brightness_buffer:
        # Color cycles based on position
        hue = (pos * 2) % 360
        return hsv(hue / 360.0, 1, brightness_buffer[index])
    
    return black
