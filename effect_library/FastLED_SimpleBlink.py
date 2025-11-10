"""SimpleBlink - Basic blinking effect

A simple effect that blinks all LEDs on and off.
Demonstrates the most basic LED control pattern.

Translated from FastLED Blink example.

Parameters (edit at top of file):
- ON_COLOR: Color when LEDs are on
- ON_FRAMES: How many frames LEDs stay on (30 = 0.5 seconds at 60fps)
- OFF_FRAMES: How many frames LEDs stay off (6 = 0.1 seconds at 60fps)
"""

# Configuration
ON_COLOR = (255, 0, 0)  # Red
ON_FRAMES = 30  # 0.5 seconds on
OFF_FRAMES = 6  # 0.1 seconds off


def render(index, frame):
    """Render one pixel"""
    cycle_length = ON_FRAMES + OFF_FRAMES
    position = frame % cycle_length
    
    if position < ON_FRAMES:
        return rgb(*ON_COLOR)
    else:
        return rgb(0, 0, 0)
