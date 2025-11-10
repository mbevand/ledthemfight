"""
DemoReel100 - FastLED's "100 lines of code" demo reel
Translated from FastLED example by Mark Kriegsman, December 2014
Cycles through 6 different patterns every 10 seconds
"""

import math
import random

# Configuration
PATTERN_DURATION = 600  # frames (10 seconds at 60fps)
NUM_PATTERNS = 6

# State
current_pattern = 0
pattern_start_frame = 0
g_hue = 0  # rotating base color

def before_frame(frame):
    global current_pattern, pattern_start_frame, g_hue
    
    # Slowly cycle the base color through the rainbow
    g_hue = (frame * 20 / 60) % 360  # Increment every 20ms equivalent
    
    # Check if it's time to switch patterns
    if frame - pattern_start_frame >= PATTERN_DURATION:
        current_pattern = (current_pattern + 1) % NUM_PATTERNS
        pattern_start_frame = frame

def render(index, frame):
    local_frame = frame - pattern_start_frame
    
    if current_pattern == 0:
        return rainbow(index)
    elif current_pattern == 1:
        return rainbow_with_glitter(index, frame)
    elif current_pattern == 2:
        return confetti(index, frame)
    elif current_pattern == 3:
        return sinelon(index, frame)
    elif current_pattern == 4:
        return juggle(index, frame)
    elif current_pattern == 5:
        return bpm(index, frame)
    
    return black

# Pattern 0: Rainbow
def rainbow(index):
    # FastLED's built-in rainbow generator
    hue = (g_hue + index * 7) % 360
    return hsv(hue / 360, 1, 1)

# Pattern 1: Rainbow with Glitter
def rainbow_with_glitter(index, frame):
    color = rainbow(index)
    # Add random sparkly glitter
    random.seed(frame * 10000 + index)
    if random.random() < 0.31:  # 80/255 chance
        return white
    return color

# Pattern 2: Confetti
# Random colored speckles that blink in and fade smoothly
confetti_brightness = {}

def confetti(index, frame):
    global confetti_brightness
    
    # Fade all pixels
    if index not in confetti_brightness:
        confetti_brightness[index] = 0
    
    confetti_brightness[index] *= 0.96  # fade by 10/255
    
    # Randomly add new sparkles
    random.seed(frame * 10000 + index)
    if random.random() < 0.05:
        hue = (g_hue + random.randint(0, 64)) % 360
        confetti_brightness[index] = 1.0
        return hsv(hue / 360, 0.78, 1)  # sat=200/255
    
    # Return faded color
    if confetti_brightness[index] > 0.01:
        hue = (g_hue + random.randint(0, 64)) % 360
        return hsv(hue / 360, 0.78, confetti_brightness[index])
    return black

# Pattern 3: Sinelon
# A colored dot sweeping back and forth with fading trails
sinelon_brightness = {}

def sinelon(index, frame):
    global sinelon_brightness
    
    # Fade all pixels
    if index not in sinelon_brightness:
        sinelon_brightness[index] = 0
    
    sinelon_brightness[index] *= 0.92  # fade by 20/255
    
    # Calculate position of the dot using beatsin
    # beatsin16(13, 0, NUM_LEDS-1)
    beat_pos = (math.sin((frame * 13 / 60) * 2 * math.pi) + 1) / 2
    pos = int(beat_pos * (num_pixels - 1))
    
    if index == pos:
        sinelon_brightness[index] = 0.75  # brightness = 192/255
        return hsv(g_hue / 360, 1, 0.75)
    
    if sinelon_brightness[index] > 0.01:
        return hsv(g_hue / 360, 1, sinelon_brightness[index])
    return black

# Pattern 4: BPM
# Colored stripes pulsing at a defined Beats-Per-Minute
def bpm(index, frame):
    beats_per_minute = 62
    # beatsin8(BeatsPerMinute, 64, 255)
    beat = (math.sin((frame * beats_per_minute / 60 / 60) * 2 * math.pi) + 1) / 2
    beat = beat * (191 / 255) + (64 / 255)  # scale to 64-255 range
    
    # Use PartyColors-like palette (cycling through rainbow)
    palette_index = (g_hue + index * 2) % 360
    brightness = beat - (g_hue + index * 10) / 360
    brightness = max(0, min(1, brightness))
    
    return hsv(palette_index / 360, 1, brightness)

# Pattern 5: Juggle
# Eight colored dots weaving in and out of sync
juggle_brightness = {}

def juggle(index, frame):
    global juggle_brightness
    
    # Fade all pixels
    if index not in juggle_brightness:
        juggle_brightness[index] = 0
    
    juggle_brightness[index] *= 0.92  # fade by 20/255
    
    # Eight dots at different speeds
    dot_hue = 0
    for i in range(8):
        # beatsin16(i+7, 0, NUM_LEDS-1)
        beat_pos = (math.sin((frame * (i + 7) / 60) * 2 * math.pi) + 1) / 2
        pos = int(beat_pos * (num_pixels - 1))
        
        if index == pos:
            juggle_brightness[index] = max(juggle_brightness[index], 1.0)
            return hsv(dot_hue / 360, 0.78, 1)  # sat=200/255
        
        dot_hue = (dot_hue + 32) % 360
    
    if juggle_brightness[index] > 0.01:
        return hsv(0, 0.78, juggle_brightness[index])
    return black
