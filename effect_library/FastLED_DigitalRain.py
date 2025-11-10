"""
DigitalRain - Binary/hex code rain effect
Like Matrix but with actual numbers/letters falling
"""

import random

# Character drops
drops = {}
MAX_DROPS = None

# Character set (as brightness patterns)
CHARS = "01"  # Binary digits

def before_frame(frame):
    global drops, MAX_DROPS
    
    if MAX_DROPS is None:
        MAX_DROPS = max(5, num_pixels // 8)
    
    # Update existing drops
    for drop_id in list(drops.keys()):
        drop = drops[drop_id]
        
        # Move drop down
        if frame % drop['speed'] == 0:
            drop['pos'] += 1
            
            # Change character occasionally
            if random.random() < 0.1:
                drop['char'] = random.choice(CHARS)
        
        # Remove if off screen
        if drop['pos'] > num_pixels + drop['length']:
            del drops[drop_id]
    
    # Add new drops
    random.seed(frame)
    if len(drops) < MAX_DROPS and random.random() < 0.15:
        drops[len(drops)] = {
            'pos': 0,
            'length': random.randint(3, 8),
            'speed': random.randint(2, 4),
            'char': random.choice(CHARS),
            'brightness': random.uniform(0.5, 1.0)
        }

def render(index, frame):
    # Check all drops
    for drop in drops.values():
        # Head position
        head = drop['pos']
        tail = head - drop['length']
        
        if tail <= index <= head:
            distance_from_head = head - index
            
            # Head is brightest
            if distance_from_head == 0:
                # Blinking head
                if frame % 4 < 2:
                    return rgb(0.9, 1, 0.9)
                else:
                    return rgb(0.5, 0.8, 0.5)
            
            # Tail fades
            fade = 1.0 - (distance_from_head / drop['length'])
            fade = fade ** 1.5
            
            # Simulate character pattern (binary blink)
            char_val = 1.0 if drop['char'] == '1' else 0.5
            brightness = fade * char_val * drop['brightness']
            
            return rgb(0, brightness * 0.7, 0)
    
    return black
