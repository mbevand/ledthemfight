"""
Noise - Perlin noise-based animation
Translated from FastLED Noise example
Creates organic, flowing patterns using procedural noise
"""

import math

# Noise parameters
SPEED = 20      # Speed of noise movement (1=very slow, 100=very fast)
SCALE = 311     # Scale of noise (lower=zoomed in, higher=zoomed out)

# Noise state
noise_x = 12345
noise_y = 67890
noise_z = 11111

def simple_perlin_noise(x, y, z):
    """
    Simplified Perlin noise implementation
    Returns value between 0 and 1
    """
    # This is a simplified noise function
    # For production, you'd want a proper Perlin noise implementation
    
    # Use sine waves to create organic-looking patterns
    val = math.sin(x * 0.1) * math.cos(y * 0.1) * math.sin(z * 0.05)
    val += math.sin(x * 0.05 + y * 0.07) * 0.5
    val += math.sin((x + y) * 0.03) * 0.3
    val += math.sin(z * 0.1) * 0.2
    
    # Normalize to 0-1
    return (val + 2) / 4

def before_frame(frame):
    global noise_z
    # Move through the noise space over time
    noise_z += SPEED

def render(index, frame):
    # Calculate noise coordinates for this pixel
    x_coord = noise_x + (SCALE * index)
    y_coord = noise_y
    z_coord = noise_z
    
    # Get noise value (0-1)
    noise_val = simple_perlin_noise(x_coord * 0.001, y_coord * 0.001, z_coord * 0.001)
    
    # Map noise to hue (full color spectrum)
    hue = noise_val
    
    # Optional: add some brightness variation
    brightness = 0.6 + noise_val * 0.4
    
    return hsv(hue, 1, brightness)
