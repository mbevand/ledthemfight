import random, math
from array import array

fwork = None
buf = None
colors = {}

class Firework:
    def __init__(self):
        self.state = 'shooting'
        self.position = 0
        self.speed = num_pixels / 70
        (a, b) = (.962, .985)
        self.speed_decay = random.random() * (b - a) + a
        self.width = round(num_pixels / 10)
        self.explode_at_speed = 1
        self.color = random.choice((red, lime, yellow, blue, magenta, cyan))
        self.part_max_speed = num_pixels / 6
    def move(self, frame):
        # make the firework explode in the middle third of the string
        e = self.position if self.speed > 0 else num_pixels - self.position
        e = e / num_pixels - 1 / 3
        if e > 0 and random.random() / 3 < e:
            self.state = 'exploding'
            self.exploding_frame = frame
            def p():
                pos = self.position
                speed = (random.random() - .5) * self.part_max_speed
                life = random.random() * 100 + 30 # frames of life
                pcol = random.choice((orange_halloween, purple))
                return (pos, speed, life, pcol)
            self.particles = [p() for i in range(round(num_pixels / 7))]
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
                buf[j] = (numerator / fwork.width)**3
                colors[j] = white
    else:
        age = frame - fwork.exploding_frame
        all_dead = True
        for (pos, speed, life, pcol) in fwork.particles:
            i = round(pos + math.log(1 + age) * speed)
            a = age - 60
            if i >= 0 and i < num_pixels and a < life:
                buf[i] += 1 if a < 0 else (life - a) / life
                colors[i] = pcol
                all_dead = False
        if all_dead:
            fwork = None

def render(index, frame):
    if not fwork:
        return black
    c = colors[index] if index in colors else black
    return rgb(*[buf[index] * _ for _ in c])
