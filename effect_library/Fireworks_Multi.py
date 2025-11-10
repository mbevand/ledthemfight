"""Multiple fireworks launching simultaneously with different color palettes

Enhanced fireworks effect with:
- Multiple fireworks launching at random intervals
- Different height trajectories
- 8 different color palettes
- Varied explosion sizes and particle counts
- More realistic physics
"""

import random, math
from array import array

fireworks = []
buf = None
colors = {}
last_launch_frame = 0

# Color palettes for variety
PALETTES = [
    # Classic Gold
    {'trail': (255, 165, 0), 'particles': [(255, 200, 0), (255, 150, 0), (255, 100, 0), (200, 50, 0)]},
    # Red/Pink
    {'trail': (255, 0, 100), 'particles': [(255, 0, 150), (255, 50, 100), (200, 0, 100), (150, 0, 50)]},
    # Blue/Cyan
    {'trail': (0, 100, 255), 'particles': [(0, 150, 255), (0, 200, 255), (0, 255, 255), (50, 200, 255)]},
    # Green
    {'trail': (0, 255, 100), 'particles': [(0, 255, 150), (50, 255, 100), (100, 255, 50), (150, 200, 0)]},
    # Purple/Magenta
    {'trail': (200, 0, 255), 'particles': [(255, 0, 255), (200, 50, 255), (150, 0, 200), (255, 0, 150)]},
    # White/Silver
    {'trail': (200, 200, 255), 'particles': [(255, 255, 255), (200, 200, 255), (150, 150, 200), (100, 100, 150)]},
    # Halloween (Orange/Purple)
    {'trail': (255, 100, 0), 'particles': [(255, 140, 0), (200, 0, 200), (150, 0, 150), (255, 50, 0)]},
    # Rainbow mix
    {'trail': (255, 255, 0), 'particles': [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255)]},
]

class Firework:
    def __init__(self, start_pos=0):
        self.state = 'shooting'
        self.position = start_pos
        
        # Variable launch speed - some go higher, some lower
        speed_factor = random.uniform(0.8, 1.8)  # More variation
        self.speed = (num_pixels / 70) * speed_factor
        
        # Variable decay rate affects height
        (a, b) = (.950, .990)
        self.speed_decay = random.random() * (b - a) + a
        
        self.width = round(num_pixels / random.uniform(8, 12))
        
        # Choose random color palette
        self.palette = random.choice(PALETTES)
        self.trail_color = self.palette['trail']
        
        # Variable particle characteristics
        self.part_max_speed = num_pixels / random.uniform(4, 9)
        self.particle_count = random.randint(round(num_pixels / 10), round(num_pixels / 4))
        
        # Variable explosion height
        self.explosion_height = random.uniform(0.35, 0.85)
        
    def move(self, frame):
        e = self.position / num_pixels
        
        if e > self.explosion_height and self.speed > 0:
            if random.random() < 0.15:  # Chance to explode
                self.state = 'exploding'
                self.exploding_frame = frame
                def p():
                    pos = self.position
                    # Varied particle speeds for more natural explosion
                    speed = (random.random() - .5) * self.part_max_speed * random.uniform(0.6, 1.4)
                    life = random.random() * 100 + 30
                    pcol = random.choice(self.palette['particles'])
                    return (pos, speed, life, pcol)
                self.particles = [p() for i in range(self.particle_count)]
        
        if self.state == 'shooting':
            self.position += self.speed
            self.speed *= self.speed_decay
            
            # Mark as dead if it goes off screen or loses momentum
            if self.position > num_pixels or self.speed < 0.1:
                self.state = 'dead'
    
    def is_dead(self, frame):
        if self.state == 'dead':
            return True
        if self.state == 'exploding':
            age = frame - self.exploding_frame
            # Check if all particles are dead
            all_dead = True
            for (pos, speed, life, pcol) in self.particles:
                i = round(pos + math.log(1 + age) * speed)
                a = age - 40
                if i >= 0 and i < num_pixels and a < life:
                    all_dead = False
                    break
            return all_dead
        return False


def before_frame(frame):
    global fireworks, buf, last_launch_frame
    buf = array('f', [0]*num_pixels)
    colors.clear()
    
    # Launch new fireworks randomly (1-3 active at a time)
    if len(fireworks) < 3 and (frame - last_launch_frame) > random.randint(30, 90):
        fireworks.append(Firework())
        last_launch_frame = frame
    
    # Remove dead fireworks
    fireworks[:] = [fw for fw in fireworks if not fw.is_dead(frame)]
    
    # Update and render all fireworks
    for fw in fireworks:
        fw.move(frame)
        
        if fw.state == 'shooting':
            for i in range(fw.width):
                j = round(fw.position - fw.width / 2 + i)
                if j >= 0 and j < num_pixels:
                    numerator = i + 1
                    brightness = (numerator / fw.width)**2.5
                    if buf[j] < brightness:  # Take brighter value
                        buf[j] = brightness
                        colors[j] = fw.trail_color
        
        elif fw.state == 'exploding':
            age = frame - fw.exploding_frame
            for (pos, speed, life, pcol) in fw.particles:
                i = round(pos + math.log(1 + age) * speed)
                a = age - 40
                if i >= 0 and i < num_pixels and a < life:
                    if a < 0:
                        brightness = 1.0
                    else:
                        brightness = ((life - a) / life)**1.5
                    
                    # Accumulate brightness
                    buf[i] = min(2.0, buf[i] + brightness)  # Cap at 2x brightness
                    colors[i] = pcol


def render(index, frame):
    if index not in colors:
        return rgb(0, 0, 0)
    c = colors[index]
    brightness = min(1.0, buf[index])  # Clamp to max brightness
    return rgb(*[int(brightness * component) for component in c])
