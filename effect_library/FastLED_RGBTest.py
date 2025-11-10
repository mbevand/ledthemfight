"""
RGBTest - RGB color calibration test
Translated from FastLED RGBCalibrate example
Shows red, green, and blue pixels to verify correct color order
"""

def render(index, frame):
    # Pattern: 1 red, 2 green, 3 blue, then repeat
    pattern_pos = index % 7
    
    if pattern_pos == 0:
        return red
    elif pattern_pos in [1, 2]:
        return green
    elif pattern_pos in [3, 4, 5]:
        return blue
    else:
        return black
