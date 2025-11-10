"""
Lava - Slow-moving lava lamp effect
Creates organic, slow-moving blobs of color
"""

import math
import random

# Lava blob parameters
NUM_BLOBS = 4

class Blob:
    def __init__(self):
        self.center = random.random() * 100
        self.speed = random.uniform(-0.3, 0.3)
        self.size = random.uniform(3, 8)
        self.hue = random.uniform(0, 0.15)  # Red-orange range

blobs = []

def before_frame(frame):
    global blobs
    
    # Initialize blobs
    if len(blobs) == 0:
        random.seed(12345)
        for i in range(NUM_BLOBS):
            blobs.append(Blob())
    
    # Move blobs
    for blob in blobs:
        blob.center += blob.speed
        
        # Wrap around
        if blob.center > num_pixels + 10:
            blob.center = -10
        elif blob.center < -10:
            blob.center = num_pixels + 10

def render(index, frame):
    # Base color (dark)
    color = [0.0, 0.0, 0.0]
    
    # Add contribution from each blob
    for blob in blobs:
        # Distance from blob center
        distance = abs(index - blob.center)
        
        # Blob intensity (Gaussian-like falloff)
        if distance < blob.size * 2:
            intensity = math.exp(-(distance ** 2) / (2 * blob.size ** 2))
            
            # Get blob color
            blob_color = hsv(blob.hue, 1, intensity)
            
            # Add to pixel color
            color[0] += blob_color[0]
            color[1] += blob_color[1]
            color[2] += blob_color[2]
    
    # Clamp values
    return rgb(min(1, color[0]), min(1, color[1]), min(1, color[2]))
