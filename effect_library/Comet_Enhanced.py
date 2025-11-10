"""Enhanced comet effect with multiple comets and color variations

Features:
- Multiple comets moving simultaneously
- Different speeds and directions
- Various color palettes (fire, ice, rainbow, toxic, etc.)
- Variable tail lengths
- Smooth blending when comets cross
"""

import random

comets = []

# Color palettes
PALETTES = {
    'fire': [(255, 0, 0), (255, 100, 0), (255, 200, 0)],  # Red to yellow
    'ice': [(0, 100, 255), (0, 200, 255), (200, 255, 255)],  # Blue to white
    'toxic': [(0, 255, 0), (100, 255, 0), (200, 255, 100)],  # Green toxic
    'purple': [(128, 0, 255), (200, 0, 255), (255, 100, 255)],  # Purple haze
    'sunset': [(255, 0, 100), (255, 100, 0), (255, 200, 0)],  # Pink to orange
    'ocean': [(0, 50, 100), (0, 100, 200), (0, 200, 255)],  # Deep to light blue
    'rainbow': [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)],
    'white': [(150, 150, 255), (200, 200, 255), (255, 255, 255)],  # Cool white
}

class Comet:
    def __init__(self):
        self.position = 0 if random.random() < 0.5 else num_pixels - 1
        self.direction = 1 if self.position == 0 else -1
        self.speed = random.uniform(0.3, 1.2)  # pixels per frame
        self.tail_length = random.randint(num_pixels // 8, num_pixels // 3)
        self.palette_name = random.choice(list(PALETTES.keys()))
        self.palette = PALETTES[self.palette_name]
        self.hue_offset = random.randint(0, 255)
        
    def update(self):
        self.position += self.direction * self.speed
        
    def is_done(self):
        if self.direction > 0:
            return self.position > num_pixels + self.tail_length
        else:
            return self.position < -self.tail_length
    
    def get_brightness(self, index):
        """Get brightness for this pixel based on comet position"""
        distance = abs(index - self.position)
        
        if distance > self.tail_length:
            return 0, None
        
        # Head is brightest, tail fades exponentially
        if distance == 0:
            brightness = 1.0
            color_idx = len(self.palette) - 1
        else:
            brightness = (1 - distance / self.tail_length) ** 2.5
            # Map distance to palette color
            color_idx = int((distance / self.tail_length) * (len(self.palette) - 1))
        
        color = self.palette[color_idx]
        return brightness, color


def before_frame(frame):
    global comets
    
    # Add new comet occasionally (max 3 at a time)
    if len(comets) < 3 and random.random() < 0.02:  # 2% chance per frame
        comets.append(Comet())
    
    # Update all comets
    for comet in comets:
        comet.update()
    
    # Remove finished comets
    comets[:] = [c for c in comets if not c.is_done()]


def render(index, frame):
    # Collect all comet contributions for this pixel
    total_r, total_g, total_b = 0, 0, 0
    max_brightness = 0
    
    for comet in comets:
        brightness, color = comet.get_brightness(index)
        if brightness > 0 and color:
            total_r += color[0] * brightness
            total_g += color[1] * brightness
            total_b += color[2] * brightness
            max_brightness = max(max_brightness, brightness)
    
    # Blend colors if multiple comets overlap
    if max_brightness > 0:
        # Normalize to prevent over-brightness
        factor = min(1.0, 1.0 / max_brightness)
        return rgb(
            int(total_r * factor),
            int(total_g * factor),
            int(total_b * factor)
        )
    
    return rgb(0, 0, 0)
