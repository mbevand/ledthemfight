"""FirstLight - Simple moving white dot

A single white LED moves along the strip from start to end, then repeats.
This is the classic "first FastLED program" that demonstrates basic control.

Translated from FastLED FirstLight example.

Parameters (edit at top of file):
- DOT_COLOR: Color of the moving dot
- DELAY_FRAMES: Frames to wait between moves (6 = 0.1 seconds at 60fps)
"""

# Configuration
DOT_COLOR = (255, 255, 255)  # White
DELAY_FRAMES = 6  # About 100ms at 60fps


def render(index, frame):
    """Render one pixel"""
    # Calculate position of moving dot
    position = (frame // DELAY_FRAMES) % num_pixels
    
    if index == position:
        return rgb(*DOT_COLOR)
    else:
        return rgb(0, 0, 0)
