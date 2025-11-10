"""HSVTest - HSV color space demonstration

Cycles through the HSV color space to demonstrate:
- Hue (color selection)
- Saturation (color intensity)
- Value (brightness)

Shows how RGB colors are generated from HSV values.
Useful for understanding color mixing and testing HSV conversions.

Translated from FastLED HSVTest example.

Parameters (edit at top of file):
- MODE: 'hue_cycle', 'saturation_demo', 'value_demo', or 'all'
- SPEED: Animation speed (1-10, higher = faster)
"""

# Configuration
MODE = 'hue_cycle'  # 'hue_cycle', 'saturation_demo', 'value_demo', 'all'
SPEED = 3


def render(index, frame):
    """Demonstrate HSV color space"""
    
    if MODE == 'hue_cycle':
        # Cycle through all hues at full saturation and value
        hue = ((frame * SPEED) % 256) / 255.0
        return hsv(hue, 1.0, 1.0)
    
    elif MODE == 'saturation_demo':
        # Show saturation gradient (gray to full color)
        # Red color with varying saturation
        saturation = (index * 255) // num_pixels / 255.0
        return hsv(0, saturation, 1.0)
    
    elif MODE == 'value_demo':
        # Show value/brightness gradient (black to bright)
        # Red color with varying brightness
        value = (index * 255) // num_pixels / 255.0
        return hsv(0, 1.0, value)
    
    elif MODE == 'all':
        # Different sections show different properties
        section = (num_pixels // 3)
        
        if index < section:
            # Section 1: Hue cycle
            hue = ((frame * SPEED + index * 10) % 256) / 255.0
            return hsv(hue, 1.0, 1.0)
        elif index < section * 2:
            # Section 2: Saturation gradient
            saturation = ((index - section) * 255) // section / 255.0
            return hsv(120 / 255.0, saturation, 1.0)  # Green
        else:
            # Section 3: Value gradient
            value = ((index - section * 2) * 255) // section / 255.0
            return hsv(240 / 255.0, 1.0, value)  # Blue
    
    return hsv(0, 0, 0)
