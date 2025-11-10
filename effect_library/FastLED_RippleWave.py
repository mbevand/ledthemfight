"""
RippleWave - Water ripple simulation
Creates expanding ripples that bounce off the edges
Inspired by FastLED Wave example
"""

import math

# Wave simulation state
wave_height = []
wave_velocity = []
DAMPENING = 0.97  # Energy loss per frame (0.9-0.99)
SPEED = 0.5       # Wave propagation speed

# Ripple trigger
last_ripple_frame = -100

def before_frame(frame):
    global wave_height, wave_velocity, last_ripple_frame
    
    # Initialize arrays
    if len(wave_height) != num_pixels:
        wave_height = [0.0] * num_pixels
        wave_velocity = [0.0] * num_pixels
    
    # Trigger new ripple every 3 seconds
    if frame - last_ripple_frame > 180:
        last_ripple_frame = frame
        import random
        random.seed(frame)
        pos = random.randint(num_pixels // 4, 3 * num_pixels // 4)
        # Create initial displacement
        for i in range(max(0, pos - 2), min(num_pixels, pos + 3)):
            wave_height[i] = -1.0
    
    # Update wave physics
    new_velocity = wave_velocity.copy()
    
    # Calculate forces (wave equation)
    for i in range(1, num_pixels - 1):
        # Acceleration is proportional to curvature
        left = wave_height[i - 1]
        center = wave_height[i]
        right = wave_height[i + 1]
        
        acceleration = ((left + right) / 2 - center) * SPEED
        new_velocity[i] += acceleration
    
    # Apply dampening and update positions
    for i in range(num_pixels):
        new_velocity[i] *= DAMPENING
        wave_height[i] += new_velocity[i]
    
    wave_velocity[:] = new_velocity

def render(index, frame):
    # Get wave height at this position
    height = wave_height[index] if index < len(wave_height) else 0
    
    # Map height to brightness (centered around 0)
    brightness = abs(height)
    brightness = min(1.0, brightness)
    
    # Color based on whether wave is up or down
    if height > 0:
        # Upward wave = cyan
        return rgb(0, brightness * 0.7, brightness)
    else:
        # Downward wave = blue
        return rgb(0, 0, brightness)
