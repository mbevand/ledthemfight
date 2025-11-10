"""
Matrix - Digital rain effect like "The Matrix"
Green falling characters/drops cascading down the strip
"""

import random

# Track falling drops: {column: {'position': y, 'tail_length': n, 'speed': s}}
drops = {}
MAX_DROPS = None

def before_frame(frame):
    global drops, MAX_DROPS
    
    if MAX_DROPS is None:
        MAX_DROPS = max(3, num_pixels // 10)
    
    # Update existing drops
    for idx in list(drops.keys()):
        drop = drops[idx]
        
        # Move drop down based on its speed
        if frame % drop['speed'] == 0:
            drop['position'] += 1
        
        # Remove drop if it's completely off screen
        if drop['position'] - drop['tail_length'] >= num_pixels:
            del drops[idx]
    
    # Add new drops randomly
    random.seed(frame)
    if len(drops) < MAX_DROPS and random.random() < 0.1:
        new_idx = len(drops)
        drops[new_idx] = {
            'position': 0,
            'tail_length': random.randint(5, 15),
            'speed': random.randint(1, 3),
            'column': random.randint(0, num_pixels - 1)
        }

def render(index, frame):
    # Check all drops to see if this pixel should be lit
    for drop in drops.values():
        if index == drop['column']:
            # Calculate position in drop
            distance_from_head = drop['position'] - (index * num_pixels / num_pixels)
            
            if distance_from_head >= 0 and distance_from_head < drop['tail_length']:
                # Head is brightest white-green
                if distance_from_head < 1:
                    return rgb(0.8, 1, 0.8)
                
                # Tail fades from bright green to dark
                fade = 1.0 - (distance_from_head / drop['tail_length'])
                fade = fade ** 1.5  # Non-linear fade
                return rgb(0, fade * 0.8, 0)
    
    # Random background sparkles for extra matrix feel
    random.seed(frame * 1000 + index)
    if random.random() < 0.01:
        return rgb(0, 0.1, 0)
    
    return black
