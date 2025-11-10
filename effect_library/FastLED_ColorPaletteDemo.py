"""ColorPaletteDemo - Demonstrates color palette usage

Shows several different color palettes cycling through them:
- RainbowColors: Full rainbow spectrum
- PurpleAndGreen: Complementary colors
- BlackAndWhiteStriped: High contrast stripes
- CloudColors: Soft blue and white
- PartyColors: Vibrant party mix
- RandomPalette: Completely random colors

The palette moves smoothly across the strip with configurable blend modes.

Translated from FastLED ColorPalette example by Mark Kriegsman.

Parameters (edit at top of file):
- UPDATES_PER_SECOND: Animation speed (100 = smooth, 10 = slow)
- BRIGHTNESS: Overall brightness 0-255
- BLEND_MODE: 'linear' for smooth blending, 'none' for distinct colors
- SECONDS_PER_PALETTE: How long to show each palette
"""

import random

# Configuration
UPDATES_PER_SECOND = 100
BRIGHTNESS = 255
BLEND_MODE = 'linear'  # 'linear' or 'none'
SECONDS_PER_PALETTE = 10

# Color Palettes (16 colors each)
PALETTES = {
    'RainbowColors': [
        (255, 0, 0), (255, 32, 0), (255, 64, 0), (255, 128, 0),
        (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128),
        (0, 255, 255), (0, 128, 255), (0, 0, 255), (64, 0, 255),
        (128, 0, 255), (255, 0, 255), (255, 0, 128), (255, 0, 64)
    ],
    'PurpleAndGreen': [
        (128, 0, 128), (64, 0, 128), (128, 0, 255), (64, 0, 128),
        (128, 0, 128), (64, 0, 128), (128, 0, 255), (64, 0, 128),
        (0, 128, 0), (0, 255, 0), (0, 128, 0), (0, 64, 0),
        (0, 128, 0), (0, 255, 0), (0, 128, 0), (0, 64, 0)
    ],
    'BlackAndWhiteStriped': [
        (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
        (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
        (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
        (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)
    ],
    'CloudColors': [
        (32, 32, 64), (64, 64, 128), (128, 128, 255), (192, 192, 255),
        (255, 255, 255), (192, 192, 255), (128, 128, 255), (64, 64, 128),
        (32, 32, 64), (64, 64, 128), (128, 128, 255), (192, 192, 255),
        (255, 255, 255), (192, 192, 255), (128, 128, 255), (64, 64, 128)
    ],
    'PartyColors': [
        (255, 0, 64), (255, 128, 0), (255, 255, 0), (0, 255, 0),
        (0, 255, 255), (0, 0, 255), (128, 0, 255), (255, 0, 128),
        (255, 0, 64), (255, 128, 0), (255, 255, 0), (0, 255, 0),
        (0, 255, 255), (0, 0, 255), (128, 0, 255), (255, 0, 128)
    ],
    'LavaColors': [
        (0, 0, 0), (32, 0, 0), (64, 0, 0), (128, 0, 0),
        (128, 32, 0), (128, 64, 0), (255, 64, 0), (255, 128, 0),
        (255, 192, 0), (255, 255, 0), (255, 255, 64), (255, 255, 128),
        (255, 255, 192), (255, 255, 255), (255, 192, 128), (255, 128, 64)
    ],
    'OceanColors': [
        (0, 0, 32), (0, 0, 64), (0, 32, 128), (0, 64, 192),
        (0, 128, 255), (32, 192, 255), (64, 255, 255), (128, 255, 255),
        (0, 128, 255), (0, 64, 192), (0, 32, 128), (0, 0, 64),
        (0, 0, 32), (0, 32, 64), (0, 64, 128), (0, 128, 192)
    ],
    'ForestColors': [
        (0, 32, 0), (0, 64, 0), (0, 128, 0), (32, 128, 0),
        (64, 128, 0), (128, 128, 0), (128, 255, 0), (64, 255, 0),
        (0, 255, 0), (0, 128, 32), (0, 64, 32), (0, 32, 16),
        (32, 64, 0), (64, 96, 0), (96, 128, 0), (128, 192, 0)
    ],
}

# State
state = {
    'current_palette_index': 0,
    'start_index': 0,
    'random_palette': None
}


def generateRandomPalette():
    """Generate completely random 16-color palette"""
    palette = []
    for _ in range(16):
        palette.append((
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ))
    return palette


def colorFromPalette(palette, index, brightness=255, blend='linear'):
    """Get color from 16-color palette with optional blending"""
    # Normalize index to 0-255 range
    idx = index % 256
    
    # Find position in 16-color palette
    pos = (idx * 16) // 256
    next_pos = (pos + 1) % 16
    
    if blend == 'linear':
        # Interpolation amount
        blend_amount = ((idx * 16) % 256) / 255.0
        
        c1 = palette[pos]
        c2 = palette[next_pos]
        
        # Blend colors
        r = int(c1[0] * (1 - blend_amount) + c2[0] * blend_amount)
        g = int(c1[1] * (1 - blend_amount) + c2[1] * blend_amount)
        b = int(c1[2] * (1 - blend_amount) + c2[2] * blend_amount)
    else:
        # No blending - nearest color
        r, g, b = palette[pos]
    
    # Apply brightness
    return (
        (r * brightness) >> 8,
        (g * brightness) >> 8,
        (b * brightness) >> 8
    )


def before_frame(frame):
    """Update animation state and palette changes"""
    # Advance the starting position (animation speed)
    state['start_index'] = (state['start_index'] + 1) % 256
    
    # Change palette periodically
    seconds = frame // 60
    if seconds % SECONDS_PER_PALETTE == 0 and frame % 60 == 0:
        state['current_palette_index'] = (state['current_palette_index'] + 1) % (len(PALETTES) + 1)
        
        # Generate new random palette when cycling back
        if state['current_palette_index'] == len(PALETTES):
            state['random_palette'] = generateRandomPalette()


def render(index, frame):
    """Render one pixel from current palette"""
    # Get current palette
    palette_names = list(PALETTES.keys())
    
    if state['current_palette_index'] < len(palette_names):
        palette_name = palette_names[state['current_palette_index']]
        palette = PALETTES[palette_name]
    else:
        # Use random palette
        if state['random_palette'] is None:
            state['random_palette'] = generateRandomPalette()
        palette = state['random_palette']
    
    # Calculate color index for this pixel
    color_index = (state['start_index'] + index * 3) % 256
    
    # Get color from palette
    color = colorFromPalette(palette, color_index, BRIGHTNESS, BLEND_MODE)
    
    return rgb(*color)
