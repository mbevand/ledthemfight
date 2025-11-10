"""
ColorTemperature - Demonstrates different color temperature effects
Translated from FastLED ColorTemperature example
Alternates between warm (tungsten) and cool (overcast sky) color temperatures
"""

import math

# Color temperature profiles (Kelvin temperature approximations)
TEMPERATURES = {
    'candle': {'r': 1.0, 'g': 0.58, 'b': 0.16},
    'tungsten': {'r': 1.0, 'g': 0.78, 'b': 0.55},
    'halogen': {'r': 1.0, 'g': 0.94, 'b': 0.88},
    'daylight': {'r': 1.0, 'g': 1.0, 'b': 1.0},
    'overcast': {'r': 0.80, 'g': 0.87, 'b': 1.0},
    'clear_blue_sky': {'r': 0.70, 'g': 0.85, 'b': 1.0},
}

DISPLAY_TIME = 600  # Frames to display each temperature (10 seconds)
BLACK_TIME = 180    # Frames of black between switches (3 seconds)

current_temp = 'tungsten'
next_temp = 'overcast'

def before_frame(frame):
    global current_temp, next_temp
    
    # Calculate which period we're in
    period = (frame // DISPLAY_TIME) % 2
    
    if period == 0:
        current_temp = 'tungsten'
    else:
        current_temp = 'overcast'

def render(index, frame):
    # Show indicator pixel in first position
    if index == 0:
        temp = TEMPERATURES[current_temp]
        return rgb(temp['r'], temp['g'], temp['b'])
    
    # Black out during transition
    local_frame = frame % DISPLAY_TIME
    if local_frame < BLACK_TIME:
        return black
    
    # Show rainbow with current color temperature applied
    # Skip first 5 pixels for spacing
    if index < 5:
        return black
    
    # Generate rainbow
    hue = ((frame // 3) + (index - 5) * 20) % 360
    base_color = hsv(hue / 360.0, 1, 1)
    
    # Apply color temperature correction
    temp = TEMPERATURES[current_temp]
    return rgb(
        base_color[0] * temp['r'],
        base_color[1] * temp['g'],
        base_color[2] * temp['b']
    )
