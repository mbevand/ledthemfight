"""
HeartBeat - Pulsing heartbeat effect
Creates a realistic double-thump heartbeat pattern
"""

import math

# Heartbeat parameters
BPM = 72  # Beats per minute
BEAT_FRAMES = int(60 * 60 / BPM)  # Frames per beat

def render(index, frame):
    # Calculate position in heartbeat cycle (0-1)
    beat_phase = (frame % BEAT_FRAMES) / BEAT_FRAMES
    
    # Create double-pulse pattern
    intensity = 0
    
    # First pulse (stronger)
    if beat_phase < 0.15:
        t = beat_phase / 0.15
        intensity = math.sin(t * math.pi) * 1.0
    # Short pause
    elif beat_phase < 0.25:
        intensity = 0
    # Second pulse (weaker)
    elif beat_phase < 0.35:
        t = (beat_phase - 0.25) / 0.10
        intensity = math.sin(t * math.pi) * 0.6
    # Long pause
    else:
        intensity = 0
    
    # Red color for heartbeat
    return rgb(intensity, 0, 0)
