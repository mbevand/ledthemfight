"""TwinkleFox - Sophisticated twinkling lights with color palettes

A beautiful twinkling effect inspired by holiday lights, featuring:
- Multiple color palettes (RetroC9, Holly, Snow, Ice, FairyLight, etc.)
- Realistic incandescent cooling (dims toward red like old bulbs)
- Variable twinkle speeds and densities per pixel
- Smooth palette transitions
- Optional auto-selected background colors

Translated from FastLED TwinkleFox example by Mark Kriegsman.

Parameters (edit at top of file):
- TWINKLE_SPEED: 0-8, how fast twinkling happens (4 = medium)
- TWINKLE_DENSITY: 0-8, how many pixels twinkle (5 = medium)
- SECONDS_PER_PALETTE: How long each palette displays
- COOL_LIKE_INCANDESCENT: True = realistic bulb cooling
- AUTO_SELECT_BACKGROUND_COLOR: True = auto background from palette
"""

import math
import random

# Configuration
TWINKLE_SPEED = 4  # 0 (very slow) to 8 (very fast)
TWINKLE_DENSITY = 5  # 0 (NONE lit) to 8 (ALL lit)
SECONDS_PER_PALETTE = 10
COOL_LIKE_INCANDESCENT = True
AUTO_SELECT_BACKGROUND_COLOR = False
BACKGROUND_COLOR = (0, 0, 0)  # Black background

# Color palettes (16 colors each)
PALETTES = {
    'RetroC9': [  # Old-school C9 tree lights: red, orange, green, blue, white
        (184, 4, 0), (144, 44, 2), (184, 4, 0), (144, 44, 2),
        (144, 44, 2), (184, 4, 0), (144, 44, 2), (184, 4, 0),
        (4, 96, 2), (4, 96, 2), (4, 96, 2), (4, 96, 2),
        (7, 7, 88), (7, 7, 88), (7, 7, 88),
        (96, 104, 32)
    ],
    'Holly': [  # Dark green with red berries
        (0, 88, 12)] * 15 + [(176, 4, 2)
    ],
    'RedGreenWhite': [
        (255, 0, 0)] * 10 + [(128, 128, 128)] * 2 + [(0, 255, 0)] * 4,
    'BlueWhite': [
        (0, 0, 255)] * 13 + [(128, 128, 128)] * 3,
    'FairyLight': [  # Warm fairy lights
        (255, 221, 180), (255, 221, 180), (255, 221, 180), (255, 221, 180),
        (127, 110, 90), (127, 110, 90), (255, 221, 180), (255, 221, 180),
        (63, 55, 45), (63, 55, 45), (255, 221, 180), (255, 221, 180),
        (255, 221, 180), (255, 221, 180), (255, 221, 180), (255, 221, 180)
    ],
    'Snow': [  # Soft blue-white snowflakes
        (48, 64, 72)] * 15 + [(224, 240, 255)],
    'Ice': [  # Cold pale blue
        (12, 16, 64)] * 12 + [(24, 32, 128), (24, 32, 128), (24, 32, 128), (80, 128, 192)],
    'RedWhite': [
        (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0),
        (128, 128, 128), (128, 128, 128), (128, 128, 128), (128, 128, 128),
        (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0),
        (128, 128, 128), (128, 128, 128), (128, 128, 128), (128, 128, 128)
    ],
    'PartyColors': [  # Rainbow party
        (255, 0, 64), (255, 128, 0), (255, 255, 0), (0, 255, 0),
        (0, 255, 255), (0, 0, 255), (128, 0, 255), (255, 0, 128),
        (255, 0, 64), (255, 128, 0), (255, 255, 0), (0, 255, 0),
        (0, 255, 255), (0, 0, 255), (128, 0, 255), (255, 0, 128)
    ],
    'RainbowColors': [
        (255, 0, 0), (255, 32, 0), (255, 64, 0), (255, 128, 0),
        (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128),
        (0, 255, 255), (0, 128, 255), (0, 0, 255), (64, 0, 255),
        (128, 0, 255), (255, 0, 255), (255, 0, 128), (255, 0, 64)
    ],
}

PALETTE_NAMES = list(PALETTES.keys())

# State
state = {
    'current_palette_index': 0,
    'current_palette': PALETTES[PALETTE_NAMES[0]],
    'target_palette': PALETTES[PALETTE_NAMES[0]],
    'palette_blend': 0.0,
    'background_color': BACKGROUND_COLOR,
    'prng_seed': 11337
}


def attackDecayWave8(i):
    """Triangle wave with fast attack, slow decay"""
    if i < 86:
        return i * 3
    else:
        i -= 86
        return 255 - (i + (i // 2))


def coolLikeIncandescent(color, phase):
    """Dim green and blue more as it fades (like incandescent bulbs)"""
    if phase < 128:
        return color
    
    cooling = (phase - 128) >> 4
    r, g, b = color
    g = max(0, g - cooling)
    b = max(0, b - cooling * 2)
    return (r, g, b)


def qsub8(value, amount):
    """Subtract with saturation at 0"""
    return max(0, value - amount)


def getAverageLight(color):
    """Get average brightness of RGB color"""
    return (color[0] + color[1] + color[2]) // 3


def nscale8_video(color, scale):
    """Scale color by factor (0-255)"""
    r, g, b = color
    return (
        (r * scale) >> 8,
        (g * scale) >> 8,
        (b * scale) >> 8
    )


def colorFromPalette(palette, index, brightness=255):
    """Get color from 16-color palette with interpolation"""
    # Normalize index to 0-255 range
    idx = index % 256
    
    # Find position in 16-color palette
    pos = (idx * 16) // 256
    next_pos = (pos + 1) % 16
    
    # Interpolation amount
    blend = ((idx * 16) % 256) / 255.0
    
    c1 = palette[pos]
    c2 = palette[next_pos]
    
    # Blend colors
    r = int(c1[0] * (1 - blend) + c2[0] * blend)
    g = int(c1[1] * (1 - blend) + c2[1] * blend)
    b = int(c1[2] * (1 - blend) + c2[2] * blend)
    
    # Apply brightness
    return (
        (r * brightness) >> 8,
        (g * brightness) >> 8,
        (b * brightness) >> 8
    )


def blendColor(c1, c2, amount):
    """Blend two colors (amount 0-255)"""
    blend = amount / 255.0
    return (
        int(c1[0] * (1 - blend) + c2[0] * blend),
        int(c1[1] * (1 - blend) + c2[1] * blend),
        int(c1[2] * (1 - blend) + c2[2] * blend)
    )


def computeOneTwinkle(ms, salt):
    """Calculate color and brightness for one twinkling pixel"""
    ticks = ms >> (8 - TWINKLE_SPEED)
    fastcycle8 = ticks & 0xFF
    slowcycle16 = ((ticks >> 8) + salt) & 0xFFFF
    
    # Add some randomness
    slowcycle16 += int(math.sin((slowcycle16 / 255.0) * 2 * math.pi) * 128) + 128
    slowcycle16 = ((slowcycle16 * 2053) + 1384) & 0xFFFF
    slowcycle8 = ((slowcycle16 & 0xFF) + (slowcycle16 >> 8)) & 0xFF
    
    bright = 0
    if ((slowcycle8 & 0x0E) // 2) < TWINKLE_DENSITY:
        bright = attackDecayWave8(fastcycle8)
    
    hue = (slowcycle8 - salt) & 0xFF
    
    if bright > 0:
        c = colorFromPalette(state['current_palette'], hue, bright)
        if COOL_LIKE_INCANDESCENT:
            c = coolLikeIncandescent(c, fastcycle8)
        return c
    else:
        return (0, 0, 0)


def before_frame(frame):
    """Update palette transitions"""
    # Change palette periodically
    palette_seconds = frame // 60
    if palette_seconds % SECONDS_PER_PALETTE == 0 and frame % 60 == 0:
        # Switch to next palette
        state['current_palette_index'] = (state['current_palette_index'] + 1) % len(PALETTE_NAMES)
        state['target_palette'] = PALETTES[PALETTE_NAMES[state['current_palette_index']]]
    
    # Gradually blend toward target palette
    state['palette_blend'] = min(1.0, state['palette_blend'] + 0.002)
    
    if state['palette_blend'] >= 1.0:
        state['current_palette'] = state['target_palette']
        state['palette_blend'] = 0.0
    
    # Auto-select background color if enabled
    if AUTO_SELECT_BACKGROUND_COLOR:
        palette = state['current_palette']
        if palette[0] == palette[1]:
            bg = palette[0]
            bglight = getAverageLight(bg)
            if bglight > 64:
                state['background_color'] = nscale8_video(bg, 16)
            elif bglight > 16:
                state['background_color'] = nscale8_video(bg, 64)
            else:
                state['background_color'] = nscale8_video(bg, 86)
        else:
            state['background_color'] = BACKGROUND_COLOR
    else:
        state['background_color'] = BACKGROUND_COLOR


def render(index, frame):
    """Render one pixel with twinkling effect"""
    # PRNG for this pixel (consistent per pixel, varies per frame)
    PRNG16 = (11337 + index * 2053 + (frame // 4)) & 0xFFFF
    
    # Generate random clock offset and speed for this pixel
    PRNG16 = ((PRNG16 * 2053) + 1384) & 0xFFFF
    myclockoffset16 = PRNG16
    
    PRNG16 = ((PRNG16 * 2053) + 1384) & 0xFFFF
    myspeedmultiplierQ5_3 = ((((PRNG16 & 0xFF) >> 4) + (PRNG16 & 0x0F)) & 0x0F) + 0x08
    
    # Calculate this pixel's adjusted clock
    clock32 = (frame * 1000) // 60  # Convert frame to pseudo-milliseconds
    myclock30 = ((clock32 * myspeedmultiplierQ5_3) >> 3) + myclockoffset16
    myunique8 = (PRNG16 >> 8) & 0xFF
    
    # Compute twinkle color
    c = computeOneTwinkle(myclock30, myunique8)
    
    # Get background color
    bg = state['background_color']
    
    # Choose brighter of twinkle or background
    cbright = getAverageLight(c)
    backgroundBrightness = getAverageLight(bg)
    deltabright = cbright - backgroundBrightness
    
    if deltabright >= 32 or bg == (0, 0, 0):
        return rgb(*c)
    elif deltabright > 0:
        blended = blendColor(bg, c, deltabright * 8)
        return rgb(*blended)
    else:
        return rgb(*bg)
