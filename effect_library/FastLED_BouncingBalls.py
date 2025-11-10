"""
BouncingBalls - Physics simulation of bouncing colored balls
Inspired by various FastLED examples
Multiple balls bounce with gravity simulation
"""

import math
import random

# Ball physics
class Ball:
    def __init__(self, start_pos, color_hue):
        self.height = start_pos
        self.velocity = 0
        self.hue = color_hue
        self.dampening = 0.90  # Energy loss on bounce
        
NUM_BALLS = 3
GRAVITY = 0.15
balls = []

def before_frame(frame):
    global balls
    
    # Initialize balls on first frame
    if len(balls) == 0:
        for i in range(NUM_BALLS):
            balls.append(Ball(
                num_pixels * (i + 1) / (NUM_BALLS + 1),
                i / NUM_BALLS
            ))
    
    # Update physics for each ball
    for ball in balls:
        # Apply gravity
        ball.velocity -= GRAVITY
        ball.height += ball.velocity
        
        # Bounce off ground
        if ball.height <= 0:
            ball.height = 0
            ball.velocity = -ball.velocity * ball.dampening
            
            # Reset if ball has lost too much energy
            if abs(ball.velocity) < 0.5:
                ball.height = num_pixels
                ball.velocity = 0

def render(index, frame):
    # Draw each ball with a soft glow
    color = [0, 0, 0]
    
    for ball in balls:
        # Calculate distance from ball center
        distance = abs(index - ball.height)
        
        # Create soft glow around ball (3 pixel radius)
        if distance < 3:
            intensity = (3 - distance) / 3
            intensity = intensity ** 2  # Square for softer falloff
            
            ball_color = hsv(ball.hue, 1, intensity)
            color[0] += ball_color[0]
            color[1] += ball_color[1]
            color[2] += ball_color[2]
    
    # Clamp values
    return rgb(min(1, color[0]), min(1, color[1]), min(1, color[2]))
