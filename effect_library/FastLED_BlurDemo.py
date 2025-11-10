"""BlurDemo - Demonstrates blur and fade effects

A bright pixel moves along the strip while being blurred and faded,
creating a smooth trailing effect. Shows how blur can create organic
motion from simple point sources.

Translated from FastLED Blur example by Zach Vorhies.

Parameters (edit at top of file):
- BLUR_AMOUNT: 0-255, how much to blur (172 = strong blur)
- FADE_AMOUNT: 0-255, how much to fade each frame (16 = slow fade)
- SPEED: How many frames between moves (2 = fast, 10 = slow)
"""

# Configuration
BLUR_AMOUNT = 172  # 0 = no blur, 255 = maximum blur
FADE_AMOUNT = 16  # How much to fade each frame
SPEED = 2  # Frames per pixel move (every other frame)

# State
state = {
    'pixels': {},  # Sparse storage of LED colors
    'position': 0
}


def blur1d(pixels, num_leds, blur_amount):
    """Blur the strip by blending neighboring pixels"""
    if blur_amount == 0:
        return pixels
    
    # Keep = (255 - blur_amount) / 2
    # Share = blur_amount / 2
    keep = ((255 - blur_amount) * 256) >> 9  # Fixed point math
    share = (blur_amount * 256) >> 9
    
    new_pixels = {}
    
    for i in range(num_leds):
        # Get current pixel and neighbors
        current = pixels.get(i, (0, 0, 0))
        left = pixels.get((i - 1) % num_leds, (0, 0, 0))
        right = pixels.get((i + 1) % num_leds, (0, 0, 0))
        
        # Blend with neighbors
        r = ((current[0] * keep) + (left[0] * share) + (right[0] * share)) >> 8
        g = ((current[1] * keep) + (left[1] * share) + (right[1] * share)) >> 8
        b = ((current[2] * keep) + (left[2] * share) + (right[2] * share)) >> 8
        
        new_color = (min(255, r), min(255, g), min(255, b))
        
        # Only store if not black (sparse storage)
        if new_color != (0, 0, 0):
            new_pixels[i] = new_color
    
    return new_pixels


def fadeToBlackBy(pixels, fade_amount):
    """Fade all pixels toward black"""
    scale = 255 - fade_amount
    new_pixels = {}
    
    for i, color in pixels.items():
        r = (color[0] * scale) >> 8
        g = (color[1] * scale) >> 8
        b = (color[2] * scale) >> 8
        
        new_color = (r, g, b)
        # Only store if not black
        if new_color != (0, 0, 0):
            new_pixels[i] = new_color
    
    return new_pixels


def before_frame(frame):
    """Update blur and fade effects"""
    # Add bright pixel at current position
    hue = ((state['position'] * 2) % 256) / 255.0
    color = hsv(hue, 1.0, 1.0)
    # Convert to 0-255 integer RGB for blur functions
    color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
    state['pixels'][state['position']] = color
    
    # Blur the strip
    state['pixels'] = blur1d(state['pixels'], num_pixels, BLUR_AMOUNT)
    
    # Fade toward black
    state['pixels'] = fadeToBlackBy(state['pixels'], FADE_AMOUNT)
    
    # Move position every SPEED frames
    if frame % SPEED == 0:
        state['position'] = (state['position'] + 1) % num_pixels


def render(index, frame):
    """Render one pixel"""
    color = state['pixels'].get(index, (0, 0, 0))
    return rgb(*color)
