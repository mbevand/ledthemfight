"""
Fire2012 - Simple one-dimensional fire animation
Translated from FastLED example by Mark Kriegsman, July 2012
Part of "Five Elements" - http://youtu.be/knWiGsmgycY
"""

import random

# Fire2012 parameters
COOLING = 55    # How much does the air cool as it rises?
                # Less cooling = taller flames. More cooling = shorter flames.
                # Default 50, suggested range 20-100

SPARKING = 120  # What chance (out of 255) is there that a new spark will be lit?
                # Higher chance = more roaring fire. Lower chance = more flickery fire.
                # Default 120, suggested range 50-200

REVERSE_DIRECTION = False

# Heat array - temperature readings at each simulation cell
heat = []

def before_frame(frame):
    global heat
    
    # Initialize heat array on first frame
    if len(heat) != num_pixels:
        heat = [0] * num_pixels
    
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
    # Map from heat cells to LED colors
    pixelnumber = (num_pixels - 1) - index if REVERSE_DIRECTION else index
    
    # Get heat value for this pixel
    temperature = heat[pixelnumber] if pixelnumber < len(heat) else 0
    
    # Convert heat to color using HeatColor approximation
    return heat_color(temperature)

def heat_color(temperature):
    """
    FastLED's HeatColor function
    Approximates a 'black body radiation' spectrum for 
    an object at the given temperature.
    """
    # Scale temperature to 0-1 range
    t = temperature / 255.0
    
    if t < 0.33:
        # Black to red
        return rgb(t * 3, 0, 0)
    elif t < 0.66:
        # Red to yellow
        return rgb(1, (t - 0.33) * 3, 0)
    else:
        # Yellow to white
        return rgb(1, 1, (t - 0.66) * 3)
