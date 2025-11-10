"""
Auto Mode Cycle - Cycles through different animation patterns
Inspired by WS2812FX auto_mode_cycle example
Each mode runs for 5 seconds before switching to the next
"""

import math

# Configuration
MODE_DURATION = 300  # frames (5 seconds at 60fps)
NUM_MODES = 8

# State
current_mode = 0
mode_start_frame = 0

def before_frame(frame):
    global current_mode, mode_start_frame
    
    # Check if it's time to switch modes
    if frame - mode_start_frame >= MODE_DURATION:
        current_mode = (current_mode + 1) % NUM_MODES
        mode_start_frame = frame

def render(index, frame):
    # Calculate local frame time within current mode
    local_frame = frame - mode_start_frame
    
    if current_mode == 0:
        # Mode 0: Static solid blue
        return rgb(0, 0.48, 1)  # 0x007BFF in RGB
    
    elif current_mode == 1:
        # Mode 1: Rainbow cycle
        hue = ((index / num_pixels) + (local_frame / 200)) % 1.0
        return hsv(hue, 1, 1)
    
    elif current_mode == 2:
        # Mode 2: Theater chase
        spacing = 3
        position = (index + int(local_frame / 3)) % spacing
        return rgb(0, 0.48, 1) if position == 0 else black
    
    elif current_mode == 3:
        # Mode 3: Breathing/Pulse
        period = 120
        phase = (local_frame % period) / period
        brightness = (math.sin(phase * 2 * math.pi) + 1) / 2
        return mul(rgb(0, 0.48, 1), brightness)
    
    elif current_mode == 4:
        # Mode 4: Color wipe (scanning)
        scan_pos = (local_frame * num_pixels / 180) % num_pixels
        return rgb(0, 0.48, 1) if index <= scan_pos else black
    
    elif current_mode == 5:
        # Mode 5: Running lights
        wave_pos = ((index + local_frame / 2) % num_pixels) / num_pixels
        brightness = (math.sin(wave_pos * math.pi * 4) + 1) / 2
        return mul(rgb(0, 0.48, 1), brightness)
    
    elif current_mode == 6:
        # Mode 6: Sparkle
        import random
        random.seed(frame * 1000 + index)  # Deterministic sparkle
        if random.random() < 0.02:  # 2% chance to sparkle
            return white
        else:
            return rgb(0, 0.24, 0.5)  # Dimmed background
    
    elif current_mode == 7:
        # Mode 7: Comet/Shooting star
        comet_length = num_pixels // 4
        comet_pos = (local_frame * 2) % (num_pixels + comet_length)
        
        if index >= comet_pos - comet_length and index <= comet_pos:
            distance_from_head = comet_pos - index
            brightness = (distance_from_head / comet_length) ** 2
            return mul(rgb(0, 0.48, 1), brightness)
        else:
            return black
    
    return black
