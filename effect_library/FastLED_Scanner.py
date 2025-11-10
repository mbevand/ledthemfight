"""
Scanner - Multiple colored scanners moving back and forth
Multiple dots bouncing at different speeds, like a parking sensor
"""

class Scanner:
    def __init__(self, speed, hue, start_pos=0):
        self.pos = start_pos
        self.speed = speed
        self.direction = 1
        self.hue = hue

# Create multiple scanners
scanners = [
    Scanner(1.0, 0.0, 0),      # Red, fast
    Scanner(0.7, 0.33, 20),    # Green, medium
    Scanner(0.5, 0.66, 40),    # Blue, slow
]

fade_buffer = {}

def before_frame(frame):
    global fade_buffer
    
    # Update each scanner
    for scanner in scanners:
        # Move scanner
        scanner.pos += scanner.speed * scanner.direction
        
        # Bounce at edges
        if scanner.pos >= num_pixels - 1:
            scanner.pos = num_pixels - 1
            scanner.direction = -1
        elif scanner.pos <= 0:
            scanner.pos = 0
            scanner.direction = 1
    
    # Fade all pixels
    new_buffer = {}
    for i in range(num_pixels):
        if i in fade_buffer:
            for color_idx in range(3):
                if fade_buffer[i][color_idx] > 0.01:
                    if i not in new_buffer:
                        new_buffer[i] = [0, 0, 0]
                    new_buffer[i][color_idx] = fade_buffer[i][color_idx] * 0.92
    
    fade_buffer = new_buffer
    
    # Add scanner positions
    for scanner in scanners:
        pos = int(scanner.pos)
        if pos not in fade_buffer:
            fade_buffer[pos] = [0, 0, 0]
        
        # Get color for this scanner
        color = hsv(scanner.hue, 1, 1)
        for i in range(3):
            fade_buffer[pos][i] = max(fade_buffer[pos][i], color[i])

def render(index, frame):
    if index in fade_buffer:
        return rgb(*fade_buffer[index])
    return black
