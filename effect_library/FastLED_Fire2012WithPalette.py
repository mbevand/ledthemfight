"""
Fire2012WithPalette - Fire simulation with customizable color palette
Translated from FastLED example by Mark Kriegsman
Allows changing fire color from traditional orange to blue, green, purple, etc.
"""

import random

# Fire2012 parameters
COOLING = 55    # How much does the air cool as it rises?
SPARKING = 120  # What chance (out of 255) is there that a new spark will be lit?
REVERSE_DIRECTION = False

# Color palettes for different fire types
PALETTES = {
    'normal': [  # Traditional orange/yellow fire
        (0, 0, 0), (0.2, 0, 0), (0.5, 0, 0), (1, 0, 0),
        (1, 0.3, 0), (1, 0.6, 0), (1, 1, 0), (1, 1, 1)
    ],
    'blue': [  # Blue/cyan fire
        (0, 0, 0), (0, 0, 0.2), (0, 0, 0.5), (0, 0.3, 1),
        (0, 0.6, 1), (0.3, 0.8, 1), (0.6, 1, 1), (1, 1, 1)
    ],
    'green': [  # Green fire (copper-based)
        (0, 0, 0), (0, 0.2, 0), (0, 0.5, 0), (0, 1, 0),
        (0.3, 1, 0.3), (0.6, 1, 0.6), (0.8, 1, 0.8), (1, 1, 1)
    ],
    'purple': [  # Purple/magenta fire
        (0, 0, 0), (0.2, 0, 0.2), (0.5, 0, 0.5), (1, 0, 1),
        (1, 0.3, 1), (1, 0.6, 1), (1, 0.8, 1), (1, 1, 1)
    ]
}

# State
heat = []
current_palette = 'normal'
palette_change_frame = 0

def before_frame(frame):
    global heat, current_palette, palette_change_frame
    
    # Initialize heat array on first frame
    if len(heat) != num_pixels:
        heat = [0] * num_pixels
    
    # Change palette every 10 seconds
    if frame - palette_change_frame > 600:
        palette_change_frame = frame
        palette_names = list(PALETTES.keys())
        current_idx = palette_names.index(current_palette)
        current_palette = palette_names[(current_idx + 1) % len(palette_names)]
    
    # Add entropy to random number generator
    random.seed(frame * 12345 + int(random.random() * 10000))
    
    # Step 1: Cool down every cell a little
    for i in range(num_pixels):
        cooldown = random.randint(0, ((COOLING * 10) // num_pixels) + 2)
        heat[i] = max(0, heat[i] - cooldown)
    
    # Step 2: Heat from each cell drifts 'up' and diffuses a little
    for k in range(num_pixels - 1, 1, -1):
        heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
    
    # Step 3: Randomly ignite new 'sparks' of heat near the bottom
    if random.randint(0, 255) < SPARKING:
        y = random.randint(0, 6)
        heat[y] = min(255, heat[y] + random.randint(160, 255))

def render(index, frame):
    pixelnumber = (num_pixels - 1) - index if REVERSE_DIRECTION else index
    
    # Get heat value for this pixel
    temperature = heat[pixelnumber] if pixelnumber < len(heat) else 0
    
    # Scale heat to palette index (0-240 for best palette results)
    color_index = int((temperature / 255.0) * 240)
    
    # Get color from current palette
    return get_palette_color(current_palette, color_index)

def get_palette_color(palette_name, index):
    """Get color from palette at given index (0-240)"""
    palette = PALETTES[palette_name]
    
    # Normalize index to palette range
    normalized = (index / 240.0) * (len(palette) - 1)
    idx = int(normalized)
    frac = normalized - idx
    
    # Blend between two palette colors
    if idx >= len(palette) - 1:
        return palette[-1]
    
    c1 = palette[idx]
    c2 = palette[idx + 1]
    
    return (
        c1[0] + (c2[0] - c1[0]) * frac,
        c1[1] + (c2[1] - c1[1]) * frac,
        c1[2] + (c2[2] - c1[2]) * frac
    )
