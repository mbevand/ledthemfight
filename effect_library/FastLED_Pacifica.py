"""
Pacifica - Gentle, blue-green ocean waves
Translated from FastLED example by Mark Kriegsman and Mary Corey March, December 2019
Inspired by the waters off the southern coast of California
"""

import math

# Color palettes - three custom blue-green palettes
# Each palette has 16 colors in RGB format
PALETTE_1 = [
    (0x00, 0x05, 0x07), (0x00, 0x04, 0x09), (0x00, 0x03, 0x0B), (0x00, 0x03, 0x0D),
    (0x00, 0x02, 0x10), (0x00, 0x02, 0x12), (0x00, 0x01, 0x14), (0x00, 0x01, 0x17),
    (0x00, 0x00, 0x19), (0x00, 0x00, 0x1C), (0x00, 0x00, 0x26), (0x00, 0x00, 0x31),
    (0x00, 0x00, 0x3B), (0x00, 0x00, 0x46), (0x14, 0x55, 0x4B), (0x28, 0xAA, 0x50)
]

PALETTE_2 = [
    (0x00, 0x05, 0x07), (0x00, 0x04, 0x09), (0x00, 0x03, 0x0B), (0x00, 0x03, 0x0D),
    (0x00, 0x02, 0x10), (0x00, 0x02, 0x12), (0x00, 0x01, 0x14), (0x00, 0x01, 0x17),
    (0x00, 0x00, 0x19), (0x00, 0x00, 0x1C), (0x00, 0x00, 0x26), (0x00, 0x00, 0x31),
    (0x00, 0x00, 0x3B), (0x00, 0x00, 0x46), (0x0C, 0x5F, 0x52), (0x19, 0xBE, 0x5F)
]

PALETTE_3 = [
    (0x00, 0x02, 0x08), (0x00, 0x03, 0x0E), (0x00, 0x05, 0x14), (0x00, 0x06, 0x1A),
    (0x00, 0x08, 0x20), (0x00, 0x09, 0x27), (0x00, 0x0B, 0x2D), (0x00, 0x0C, 0x33),
    (0x00, 0x0E, 0x39), (0x00, 0x10, 0x40), (0x00, 0x14, 0x50), (0x00, 0x18, 0x60),
    (0x00, 0x1C, 0x70), (0x00, 0x20, 0x80), (0x10, 0x40, 0xBF), (0x20, 0x60, 0xFF)
]

# State variables
s_ci_start1 = 0
s_ci_start2 = 0
s_ci_start3 = 0
s_ci_start4 = 0
s_last_frame = 0

# Buffer to accumulate wave layers
wave_buffer = {}

def beatsin16(bpm, low, high, frame):
    """Approximation of FastLED's beatsin16 function"""
    beats = frame * bpm / 60 / 60  # Convert frame to beats
    sine_val = (math.sin(beats * 2 * math.pi) + 1) / 2
    return int(low + sine_val * (high - low))

def beatsin8(bpm, low, high, frame):
    """8-bit version of beatsin"""
    beats = frame * bpm / 60 / 60
    sine_val = (math.sin(beats * 2 * math.pi) + 1) / 2
    return int(low + sine_val * (high - low))

def beatsin88(bpm, low, high, frame):
    """88-bit fixed point approximation"""
    beats = frame * bpm / 60 / 60
    sine_val = (math.sin(beats * 2 * math.pi) + 1) / 2
    return low + sine_val * (high - low)

def sin16(angle):
    """16-bit sine approximation, returns -32768 to 32767"""
    normalized = (angle / 65536.0) * 2 * math.pi
    return int(math.sin(normalized) * 32767)

def scale16(value, scale):
    """Scale a 16-bit value by a 16-bit scale factor"""
    return int((value * scale) / 65536)

def get_palette_color(palette, index, brightness):
    """Get color from palette at index with brightness"""
    # Wrap index to palette size
    idx = int(index * len(palette) / 256) % len(palette)
    color = palette[idx]
    bri = brightness / 255.0
    return (color[0] / 255.0 * bri, color[1] / 255.0 * bri, color[2] / 255.0 * bri)

def before_frame(frame):
    global s_ci_start1, s_ci_start2, s_ci_start3, s_ci_start4, s_last_frame, wave_buffer
    
    # Calculate delta time
    delta_frames = frame - s_last_frame
    s_last_frame = frame
    deltams = delta_frames * 16.67  # Approximate milliseconds
    
    # Update wave counters with varying speeds
    speedfactor1 = beatsin16(3, 179, 269, frame)
    speedfactor2 = beatsin16(4, 179, 269, frame)
    deltams1 = (deltams * speedfactor1) / 256
    deltams2 = (deltams * speedfactor2) / 256
    deltams21 = (deltams1 + deltams2) / 2
    
    s_ci_start1 += int(deltams1 * beatsin88(1011, 10, 13, frame))
    s_ci_start2 -= int(deltams21 * beatsin88(777, 8, 11, frame))
    s_ci_start3 -= int(deltams1 * beatsin88(501, 5, 7, frame))
    s_ci_start4 -= int(deltams2 * beatsin88(257, 4, 6, frame))
    
    # Keep values in reasonable range
    s_ci_start1 = s_ci_start1 % 65536
    s_ci_start2 = s_ci_start2 % 65536
    s_ci_start3 = s_ci_start3 % 65536
    s_ci_start4 = s_ci_start4 % 65536
    
    # Clear buffer - start with dim background blue-green
    wave_buffer = {i: [2/255, 6/255, 10/255] for i in range(num_pixels)}
    
    # Render four wave layers with different parameters
    add_wave_layer(PALETTE_1, s_ci_start1, beatsin16(3, 11 * 256, 14 * 256, frame), 
                   beatsin8(10, 70, 130, frame), -beatsin16(301, 0, 65535, frame), frame)
    add_wave_layer(PALETTE_2, s_ci_start2, beatsin16(4, 6 * 256, 9 * 256, frame),
                   beatsin8(17, 40, 80, frame), beatsin16(401, 0, 65535, frame), frame)
    add_wave_layer(PALETTE_3, s_ci_start3, 6 * 256,
                   beatsin8(9, 10, 38, frame), -beatsin16(503, 0, 65535, frame), frame)
    add_wave_layer(PALETTE_3, s_ci_start4, 5 * 256,
                   beatsin8(8, 10, 28, frame), beatsin16(601, 0, 65535, frame), frame)
    
    # Add whitecaps where waves line up
    add_whitecaps(frame)

def add_wave_layer(palette, cistart, wavescale, bri, ioff, frame):
    """Add one layer of waves into the buffer"""
    global wave_buffer
    
    ci = cistart
    waveangle = ioff
    wavescale_half = (wavescale // 2) + 20
    
    for i in range(num_pixels):
        waveangle += 250
        waveangle = waveangle % 65536
        
        s16 = sin16(waveangle) + 32768
        cs = scale16(s16, wavescale_half) + wavescale_half
        ci += cs
        ci = ci % 65536
        
        sindex16 = sin16(ci) + 32768
        sindex8 = scale16(sindex16, 240)
        
        c = get_palette_color(palette, sindex8, bri)
        
        # Add to buffer
        wave_buffer[i][0] = min(1.0, wave_buffer[i][0] + c[0])
        wave_buffer[i][1] = min(1.0, wave_buffer[i][1] + c[1])
        wave_buffer[i][2] = min(1.0, wave_buffer[i][2] + c[2])

def add_whitecaps(frame):
    """Add extra 'white' to areas where waves line up brightly"""
    global wave_buffer
    
    basethreshold = beatsin8(9, 55, 65, frame)
    wave = beatsin8(7, 0, 255, frame)
    
    for i in range(num_pixels):
        threshold = int(math.sin(wave / 255.0 * math.pi) * 20) + basethreshold
        
        # Get brightness of current pixel
        brightness = max(wave_buffer[i][0], wave_buffer[i][1], wave_buffer[i][2]) * 255
        
        if brightness > threshold:
            overage = (brightness - threshold) / 255.0
            overage2 = overage * overage * 0.1
            wave_buffer[i][0] = min(1.0, wave_buffer[i][0] + overage2)
            wave_buffer[i][1] = min(1.0, wave_buffer[i][1] + overage2)
            wave_buffer[i][2] = min(1.0, wave_buffer[i][2] + overage2)

def render(index, frame):
    # Return accumulated color from buffer
    if index in wave_buffer:
        color = wave_buffer[index]
        # Deepen blues and greens
        return rgb(color[0], color[1] * 0.95, color[2] * 0.95)
    return rgb(2/255, 6/255, 10/255)
