import random, math
from array import array

fwork = None
buf = None
colors = {}

# Color palettes for variety
PALETTES = [
    # Classic fireworks
    {'trail': (255, 165, 0), 'particles': [(255, 200, 0), (255, 150, 0), (255, 100, 0), (200, 50, 0)]},  # Orange/Gold
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
    def __init__(self):
        self.state = 'shooting'
        self.position = 0
        
        # Variable launch speed - some go higher, some lower
        speed_factor = random.uniform(0.8, 1.5)  # 80% to 150% of base speed
        self.speed = (num_pixels / 70) * speed_factor
        
        # Variable decay rate affects height
        (a, b) = (.955, .988)  # Wider range for more variation
        self.speed_decay = random.random() * (b - a) + a
        
        self.width = round(num_pixels / 10)
        self.explode_at_speed = 1
        
        # Choose random color palette
        self.palette = random.choice(PALETTES)
        self.trail_color = self.palette['trail']
        
        # Variable particle characteristics
        self.part_max_speed = num_pixels / random.uniform(4, 8)  # Some spread faster
        self.particle_count = random.randint(round(num_pixels / 10), round(num_pixels / 5))  # Variable particle count
        
    def move(self, frame):
        # Make firework explode at different heights
        e = self.position if self.speed > 0 else num_pixels - self.position
        e = e / num_pixels
        
        # Variable explosion height (between 30% and 80% of strip)
        explosion_threshold = random.uniform(0.3, 0.8)
        
        if e > explosion_threshold and random.random() / 3 < (e - explosion_threshold):
            self.state = 'exploding'
            self.exploding_frame = frame
            def p():
                pos = self.position
                # Varied particle speeds for more natural explosion
                speed = (random.random() - .5) * self.part_max_speed * random.uniform(0.7, 1.3)
                life = random.random() * 80 + 40  # frames of life (varied)
                pcol = random.choice(self.palette['particles'])
                return (pos, speed, life, pcol)
            self.particles = [p() for i in range(self.particle_count)]
        else:
            self.position += self.speed
            self.speed *= self.speed_decay

def before_frame(frame):
    global fwork, buf
    buf = array('f', [0]*num_pixels)
    colors.clear()
    if not fwork:
        fwork = Firework()
    if fwork.state == 'shooting':
        fwork.move(frame)
        for i in range(fwork.width):
            j = round(fwork.position - fwork.width / 2 + i)
            if j >= 0 and j < num_pixels:
                numerator = i + 1 if fwork.speed > 0 else fwork.width - i
                # Brighter trail with gradient
                buf[j] = (numerator / fwork.width)**2.5
                colors[j] = fwork.trail_color
    else:
        age = frame - fwork.exploding_frame
        all_dead = True
        for (pos, speed, life, pcol) in fwork.particles:
            # Physics: particles slow down and spread out
            i = round(pos + math.log(1 + age) * speed)
            a = age - 40  # Delay before fade starts
            if i >= 0 and i < num_pixels and a < life:
                # Brightness calculation with smoother fade
                if a < 0:
                    brightness = 1.0
                else:
                    # Exponential fade looks more natural
                    brightness = ((life - a) / life)**1.5
                
                # Accumulate brightness (allows overlapping particles)
                buf[i] += brightness
                colors[i] = pcol
                all_dead = False
        if all_dead:
            fwork = None

def render(index, frame):
    if not fwork:
        return black
    c = colors[index] if index in colors else black
    return rgb(*[buf[index] * _ for _ in c])
