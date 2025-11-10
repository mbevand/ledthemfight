"""
ColorWaves - Animated color palette waves
Simplified from FastLED ColorPalette example
Shows smooth color transitions using palette blending
"""

import math

# Different color palettes to cycle through
PALETTES = {
    'rainbow': lambda i: hsv(i % 1.0, 1, 1),
    'ocean': lambda i: hsv((0.5 + i * 0.2) % 1.0, 1, 1),
    'lava': lambda i: hsv((i * 0.1) % 0.15, 1, 1),
    'forest': lambda i: hsv((0.25 + i * 0.15) % 0.4, 0.9, 0.8),
    'party': lambda i: hsv((i * 3) % 1.0, 0.9, 1),
}

current_palette = 'rainbow'
palette_index = 0

def before_frame(frame):
    global current_palette, palette_index
    
    # Change palette every 5 seconds
    if frame % 300 == 0:
        palette_names = list(PALETTES.keys())
        palette_index = (palette_index + 1) % len(palette_names)
        current_palette = palette_names[palette_index]

def render(index, frame):
    # Create moving waves through the palette
    palette_func = PALETTES[current_palette]
    
    # Multiple wave speeds for interesting patterns
    wave1 = frame / 200.0
    wave2 = frame / 333.0
    
    # Blend position in palette based on pixel index and waves
    palette_pos = (index / num_pixels + wave1 + math.sin(wave2 * 2 * math.pi) * 0.3) % 1.0
    
    return palette_func(palette_pos)
