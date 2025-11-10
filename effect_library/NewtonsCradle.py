"""Newton's Cradle - Physics simulation with collision detection

Newton's Cradle effect with realistic collision physics.
Balls have dimensions and exchange velocities on collision.

Features:
- Multiple ball counts (5, 10, 15) - randomized each cycle
- Two boundary modes - randomized each cycle:
  * wraparound: circular strip (balls wrap around edges)
  * wall: balls bounce off ends (reverse velocity)
- Configurable initial states (touching/spread balls, moving/stationary)
- Optional color palettes that change on collision:
  * Standard mode: striker gets random color from palette on each collision
  * Infect mode: initially moving balls get colors, stationary start white,
    fastest ball "infects" slower balls with its color on each strike
- Palettes: rainbow, warm, cool, fire, ocean, white
"""

import math
import random

# Configuration
BALL_SIZE = 8  # LEDs long (diameter of each ball)
INITIAL_VELOCITY = 1.5  # LEDs per frame for the initially moving ball
RESET_INTERVAL = 1200  # Frames before resetting (600 = 10 seconds at 60fps)
# BALL_COUNT_OPTIONS = [5, 10, 15]  # Different number of balls to choose from
BALL_COUNT_OPTIONS = [5, 10, 15]  # Different number of balls to choose from
BOUNDARY_MODES = ["wraparound", "wall"]  # "wraparound" = circular strip, "wall" = bounce off ends

# Color configuration
# Set to empty string "" to keep balls with random colors from palette
# Options: "rainbow", "warm", "cool", "fire", "ocean", "white"
RANDOMIZING_PALETTE = "fire"  # Empty = random from all palettes
INFECT = True  # If True, fastest ball "infects" slower ball with its color on collision

# Color palettes (hue values 0.0-1.0)
COLOR_PALETTES = {
    "rainbow": [0.0, 0.15, 0.33, 0.5, 0.66, 0.83],  # Full rainbow spectrum
    "warm": [0.0, 0.05, 0.1, 0.15],  # Reds, oranges, yellows
    "cool": [0.5, 0.55, 0.6, 0.7],  # Cyans, blues, purples
    "fire": [0.0, 0.05, 0.08, 0.12, 0.15],  # Fire colors
    "ocean": [0.45, 0.5, 0.55, 0.6],  # Ocean blues and greens
    "white": [0.0],  # White/grayscale (saturation will be 0)
}

# Ball state
balls = []
initialized = False
frame_counter = 0
current_num_balls = 15  # Will be set randomly on each reset
current_boundary_mode = "wraparound"  # Will be set randomly on each reset

# Pre-filled table of random initial configurations for different ball counts
# Key: number of balls, Value: list of configs
# Each config is a list of (spacing_multiplier, has_velocity, velocity_multiplier) tuples
# spacing_multiplier: 0.0 = touching, 1.0 = spread evenly
# has_velocity: True if ball is initially moving
# velocity_multiplier: Speed multiplier (0.5 = half speed, 1.0 = normal, 1.5 = 1.5x speed, etc.)
INITIAL_CONFIGS_BY_COUNT = {
    5: [
        # Config 0: Classic - single ball from left, rest touching
        [(1.0, True, 1.0), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0)],
        # Config 1: Two balls from opposite ends, different speeds
        [(1.0, True, 1.2), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (1.0, True, 0.8)],
        # Config 2: Three movers - two from left at different speeds, one from right
        [(1.0, True, 1.5), (0.5, True, 1.0), (0.0, False, 0.0), (0.0, False, 0.0), (1.0, True, 1.0)],
        # Config 3: All spread, three movers at different speeds
        [(1.0, True, 0.7), (1.0, False, 0.0), (1.0, True, 1.3), (1.0, False, 0.0), (1.0, True, 1.0)],
        # Config 4: Two groups - touching pair and spread movers
        [(1.0, True, 1.2), (1.0, True, 0.8), (0.5, False, 0.0), (0.0, True, 1.0), (0.0, False, 0.0)],
        # Config 5: Chaos - four movers at various speeds
        [(1.0, True, 0.6), (0.8, True, 1.4), (0.6, False, 0.0), (1.0, True, 1.1), (0.7, True, 0.9)],
        # Config 6: Three touching on left, two movers on right
        [(0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (1.0, True, 1.3), (0.8, True, 0.7)],
        # Config 7: Alternating movers and stationary, all spread
        [(1.0, True, 1.1), (1.0, False, 0.0), (1.0, True, 0.9), (1.0, False, 0.0), (1.0, True, 1.2)],
        # Config 8: Two groups of touching balls, one mover each side
        [(1.0, True, 1.0), (0.0, False, 0.0), (0.0, False, 0.0), (1.0, False, 0.0), (0.0, True, 1.0)],
        # Config 9: All movers, tightly packed, varying speeds
        [(0.3, True, 0.8), (0.3, True, 1.2), (0.3, True, 0.6), (0.3, True, 1.4), (0.3, True, 1.0)],
    ],
    10: [
        # Config 0: Classic - single mover from left, rest touching
        [(1.0, True, 1.0)] + [(0.0, False, 0.0)] * 9,
        # Config 1: Two from opposite ends, different speeds
        [(1.0, True, 1.3), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0),
         (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (1.0, True, 0.7)],
        # Config 2: Four movers from left side, varying speeds
        [(1.0, True, 1.5), (0.7, True, 1.2), (0.5, True, 0.9), (0.3, True, 0.6)] + [(0.0, False, 0.0)] * 6,
        # Config 3: Three groups - touching clusters with movers
        [(1.0, True, 1.1), (0.0, False, 0.0), (0.0, True, 0.8), (1.0, False, 0.0), (0.0, False, 0.0),
         (0.0, True, 1.2), (1.0, False, 0.0), (0.0, False, 0.0), (0.0, True, 1.0), (0.0, False, 0.0)],
        # Config 4: Five movers, all spread evenly, different speeds
        [(1.0, True, 0.7), (1.0, False, 0.0), (1.0, True, 1.3), (1.0, False, 0.0), (1.0, True, 1.0),
         (1.0, False, 0.0), (1.0, True, 0.8), (1.0, False, 0.0), (1.0, True, 1.2), (1.0, False, 0.0)],
        # Config 5: Six movers, scattered positioning and speeds
        [(1.0, True, 1.4), (0.8, True, 0.9), (0.5, False, 0.0), (1.0, True, 1.1), (0.6, True, 0.7),
         (0.4, False, 0.0), (1.0, True, 1.3), (0.7, True, 0.8), (0.5, False, 0.0), (0.3, False, 0.0)],
        # Config 6: Two large groups, movers at edges and middle
        [(1.0, True, 1.2), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, True, 0.9), (0.0, False, 0.0),
         (0.0, True, 1.1), (1.0, False, 0.0), (0.0, False, 0.0), (0.0, True, 0.8), (0.0, False, 0.0)],
        # Config 7: Four movers in center, stationary on edges
        [(1.0, False, 0.0), (1.0, False, 0.0), (0.8, True, 1.3), (0.6, True, 0.8), (0.5, True, 1.1),
         (0.5, True, 0.9), (0.8, False, 0.0), (1.0, False, 0.0), (1.0, False, 0.0), (1.0, False, 0.0)],
        # Config 8: Alternating groups - touching and spread with movers
        [(0.0, True, 1.0), (0.0, False, 0.0), (1.0, True, 1.2), (1.0, False, 0.0), (0.0, True, 0.8),
         (0.0, False, 0.0), (1.0, True, 1.1), (1.0, False, 0.0), (0.0, True, 0.9), (0.0, False, 0.0)],
        # Config 9: Chaos - seven movers, tight packing, wide speed range
        [(0.4, True, 0.6), (0.4, True, 1.5), (0.4, False, 0.0), (0.4, True, 1.0), (0.4, True, 0.7),
         (0.4, True, 1.3), (0.4, False, 0.0), (0.4, True, 0.9), (0.4, True, 1.2), (0.4, False, 0.0)],
    ],
    15: [
        # Config 0: Classic - single mover from left, all touching
        [(1.0, True, 1.0)] + [(0.0, False, 0.0)] * 14,
        # Config 1: Two from opposite ends, different speeds
        [(1.0, True, 1.4)] + [(0.0, False, 0.0)] * 13 + [(1.0, True, 0.6)],
        # Config 2: Five movers from left, varying speeds and spacing
        [(1.0, True, 1.5), (0.8, True, 1.3), (0.6, True, 1.0), (0.4, True, 0.7), (0.3, True, 0.5)] + [(0.0, False, 0.0)] * 10,
        # Config 3: Seven movers, all spread evenly, varying speeds
        [(1.0, True, 0.7), (1.0, False, 0.0), (1.0, True, 1.3), (1.0, False, 0.0), (1.0, True, 1.0),
         (1.0, False, 0.0), (1.0, True, 0.8), (1.0, False, 0.0), (1.0, True, 1.2), (1.0, False, 0.0),
         (1.0, True, 0.9), (1.0, False, 0.0), (1.0, True, 1.1), (1.0, False, 0.0), (1.0, False, 0.0)],
        # Config 4: Four groups of touching balls with movers
        [(1.0, True, 1.2), (0.0, False, 0.0), (0.0, True, 0.9), (0.0, False, 0.0), (1.0, False, 0.0),
         (0.0, True, 1.1), (0.0, False, 0.0), (0.0, False, 0.0), (1.0, True, 0.8), (0.0, False, 0.0),
         (0.0, False, 0.0), (1.0, True, 1.3), (0.0, False, 0.0), (0.0, True, 1.0), (0.0, False, 0.0)],
        # Config 5: Eight movers, scattered positions, wide speed variety
        [(1.0, True, 1.5), (0.8, True, 0.8), (0.6, False, 0.0), (1.0, True, 1.2), (0.5, True, 0.6),
         (0.4, False, 0.0), (1.0, True, 1.4), (0.7, True, 0.9), (0.5, False, 0.0), (1.0, True, 1.1),
         (0.6, True, 0.7), (0.4, False, 0.0), (0.8, True, 1.3), (0.5, True, 1.0), (0.3, False, 0.0)],
        # Config 6: Three large groups, movers between and at edges
        [(1.0, True, 1.1), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, True, 0.9),
         (1.0, False, 0.0), (0.0, False, 0.0), (0.0, False, 0.0), (0.0, True, 1.2), (1.0, False, 0.0),
         (0.0, False, 0.0), (0.0, False, 0.0), (0.0, True, 0.8), (0.0, False, 0.0), (0.0, False, 0.0)],
        # Config 7: Six movers in pairs, different speeds
        [(1.0, True, 1.3), (0.8, True, 1.0), (1.0, False, 0.0), (1.0, False, 0.0), (1.0, True, 0.7),
         (0.8, True, 1.1), (1.0, False, 0.0), (1.0, False, 0.0), (1.0, True, 1.2), (0.8, True, 0.8),
         (1.0, False, 0.0), (1.0, False, 0.0), (1.0, True, 0.9), (0.8, True, 1.4), (1.0, False, 0.0)],
        # Config 8: Ten movers, tight spacing, extreme speed variation
        [(0.5, True, 0.5), (0.5, True, 1.6), (0.5, False, 0.0), (0.5, True, 1.0), (0.5, True, 0.7),
         (0.5, True, 1.4), (0.5, False, 0.0), (0.5, True, 0.9), (0.5, True, 1.3), (0.5, False, 0.0),
         (0.5, True, 0.6), (0.5, True, 1.2), (0.5, False, 0.0), (0.5, True, 1.1), (0.5, False, 0.0)],
        # Config 9: Alternating single and touching pairs with movers
        [(1.0, True, 1.0), (1.0, False, 0.0), (0.0, True, 1.2), (0.0, False, 0.0), (1.0, True, 0.8),
         (1.0, False, 0.0), (0.0, True, 1.1), (0.0, False, 0.0), (1.0, True, 0.9), (1.0, False, 0.0),
         (0.0, True, 1.3), (0.0, False, 0.0), (1.0, True, 0.7), (1.0, False, 0.0), (0.0, False, 0.0)],
    ],
}

class Ball:
    def __init__(self, position, velocity=0.0):
        self.position = position  # Center position (float)
        self.velocity = velocity  # LEDs per frame (float)
        self.mass = 1.0  # All balls have identical mass
        self.hue = 0.0  # Color hue (0.0-1.0)
        self.saturation = 0.0  # Color saturation (0.0 = white/gray, 1.0 = full color)
        
    @property
    def left_edge(self):
        """Left edge of the ball"""
        return self.position - BALL_SIZE / 2.0
    
    @property
    def right_edge(self):
        """Right edge of the ball"""
        return self.position + BALL_SIZE / 2.0


def init_balls():
    """Initialize balls with random count and configuration"""
    global balls, initialized, current_num_balls, current_boundary_mode
    
    # Randomly choose number of balls for this cycle
    current_num_balls = random.choice(BALL_COUNT_OPTIONS)
    
    # Randomly choose boundary mode for this cycle
    current_boundary_mode = random.choice(BOUNDARY_MODES)
    
    # Get configs for this ball count
    available_configs = INITIAL_CONFIGS_BY_COUNT.get(current_num_balls, [])
    if not available_configs:
        # Fallback: create a simple config if none exists
        available_configs = [[(1.0, i == 0) for i in range(current_num_balls)]]
    
    # Choose a random configuration
    config = random.choice(available_configs)
    
    # Determine palette to use
    if RANDOMIZING_PALETTE and RANDOMIZING_PALETTE in COLOR_PALETTES:
        palette = COLOR_PALETTES[RANDOMIZING_PALETTE]
        is_white_palette = (RANDOMIZING_PALETTE == "white")
    else:
        # No palette specified - use white
        palette = COLOR_PALETTES["white"]
        is_white_palette = True
    
    # Spread balls along the strip with spacing based on config
    margin = BALL_SIZE
    usable_length = num_pixels - 2 * margin
    
    # Calculate base spacing (for multiplier = 1.0)
    base_spacing = usable_length / (current_num_balls - 1) if current_num_balls > 1 else 0
    
    balls = []
    current_pos = margin
    
    for i in range(current_num_balls):
        spacing_mult, has_velocity, velocity_mult = config[i]
        
        # Determine velocity for this ball
        vel = 0.0
        if has_velocity:
            # Random direction (left or right)
            direction = random.choice([-1, 1])
            vel = INITIAL_VELOCITY * velocity_mult * direction
        
        new_ball = Ball(current_pos, vel)
        
        # Assign color to all balls from palette
        new_ball.hue = random.choice(palette)
        new_ball.saturation = 0.0 if is_white_palette else 1.0
        
        # In INFECT mode, only initially moving balls get saturated colors
        # Stationary balls start as white
        if INFECT and not has_velocity:
            new_ball.saturation = 0.0
        
        balls.append(new_ball)
        
        # Move to next position (except for last ball)
        if i < current_num_balls - 1:
            if spacing_mult == 0.0:
                # Touching: distance between centers = BALL_SIZE (diameter)
                current_pos += BALL_SIZE
            else:
                # Spaced: use the spacing multiplier
                current_pos += base_spacing * spacing_mult
    
    # Ensure no balls overlap initially (safety check)
    for i in range(len(balls) - 1):
        if balls[i + 1].position - balls[i].position < BALL_SIZE:
            balls[i + 1].position = balls[i].position + BALL_SIZE
    
    initialized = True


def reset_animation():
    """Reset the animation with new random configuration"""
    global initialized, frame_counter
    initialized = False
    frame_counter = 0


def check_collisions():
    """Detect and handle collisions between balls"""
    # Sort balls by position
    sorted_balls = sorted(balls, key=lambda b: b.position)
    
    # Determine how many pairs to check based on boundary mode
    num_pairs = len(sorted_balls) if current_boundary_mode == "wraparound" else len(sorted_balls) - 1
    
    # Check each pair of adjacent balls (in position order)
    for i in range(num_pairs):
        ball_a = sorted_balls[i]
        
        if i == len(sorted_balls) - 1:
            # Last ball - only check wraparound in wraparound mode
            if current_boundary_mode != "wraparound":
                continue
            ball_b = sorted_balls[0]  # Wrap around to first ball
            # Check wraparound distance
            distance_normal = ball_b.position + num_pixels - ball_a.position
            distance_wrap = ball_b.position - ball_a.position
            distance = min(distance_normal, abs(distance_wrap))
        else:
            # Normal adjacent balls
            ball_b = sorted_balls[i + 1]
            distance = ball_b.position - ball_a.position
        
        # Two balls with diameter BALL_SIZE are touching when their centers are BALL_SIZE apart
        # They overlap when distance < BALL_SIZE
        if distance < BALL_SIZE:
            # Only process collision if balls are approaching each other
            relative_velocity = ball_a.velocity - ball_b.velocity
            
            if relative_velocity > 0:  # Balls are approaching
                # Determine which ball is moving faster BEFORE swapping velocities
                # (needed for color changes)
                if abs(ball_a.velocity) > abs(ball_b.velocity):
                    faster_ball = ball_a
                    slower_ball = ball_b
                else:
                    faster_ball = ball_b
                    slower_ball = ball_a
                
                # Collision! Exchange velocities (elastic collision with equal masses)
                ball_a.velocity, ball_b.velocity = ball_b.velocity, ball_a.velocity
                
                # Separate balls so they're exactly touching (distance = BALL_SIZE)
                overlap = BALL_SIZE - distance
                ball_a.position -= overlap / 2.0
                ball_b.position += overlap / 2.0
                
                # Handle color changes on collision
                if RANDOMIZING_PALETTE and RANDOMIZING_PALETTE in COLOR_PALETTES:
                    palette = COLOR_PALETTES[RANDOMIZING_PALETTE]
                    is_white_palette = (RANDOMIZING_PALETTE == "white")
                    
                    if INFECT:
                        # Step 4: INFECT mode - fastest ball infects the other with its color
                        # If the faster ball has color (saturation > 0), infect the slower ball
                        if faster_ball.saturation > 0:
                            slower_ball.hue = faster_ball.hue
                            slower_ball.saturation = faster_ball.saturation
                    else:
                        # Step 3: Standard mode - randomize color of striking ball
                        new_hue = random.choice(palette)
                        
                        # Color the ball that was moving faster (the striker)
                        faster_ball.hue = new_hue
                        faster_ball.saturation = 0.0 if is_white_palette else 1.0


def update_physics():
    """Update ball positions and velocities"""
    # Move all balls according to their velocities
    for ball in balls:
        ball.position += ball.velocity
        
        # Handle boundary conditions based on current mode
        if current_boundary_mode == "wraparound":
            # Wraparound: if ball goes off one end, appear at the other end
            if ball.position < 0:
                ball.position += num_pixels
            elif ball.position >= num_pixels:
                ball.position -= num_pixels
        else:  # wall mode
            # Wall: bounce off the ends by reversing velocity
            half_ball = BALL_SIZE / 2.0
            if ball.position - half_ball <= 0:
                # Hit left wall
                ball.position = half_ball
                ball.velocity = -ball.velocity
            elif ball.position + half_ball >= num_pixels:
                # Hit right wall
                ball.position = num_pixels - half_ball
                ball.velocity = -ball.velocity
    
    # Check for collisions and handle them
    check_collisions()


def before_frame(frame):
    """Initialize and update ball physics"""
    global frame_counter
    
    if not initialized:
        init_balls()
    
    # Check if it's time to reset
    if frame_counter >= RESET_INTERVAL:
        reset_animation()
        return
    
    update_physics()
    frame_counter += 1


def render(index, frame):
    """Render the Newton's Cradle with colored or white balls"""
    # Background is black
    total_brightness = 0
    total_hue = 0.0
    total_saturation = 0.0
    
    for ball in balls:
        # Calculate distance from this pixel to ball center
        distance = abs(index - ball.position)
        radius = BALL_SIZE / 2.0
        core = radius * 0.9
        
        # Create soft glow around ball
        brightness = 0
        if distance < core:
            # Core of ball is bright
            brightness = 1.0 - (distance / core) ** 2
        elif distance < radius:
            # Outer glow
            outer_distance = distance - core
            brightness = 0.8 * (1.0 - (outer_distance / (radius - core)))
        
        if brightness > 0:
            total_brightness += brightness
            # Accumulate hue weighted by saturation and brightness
            total_hue += ball.hue * brightness * ball.saturation
            total_saturation += ball.saturation * brightness
    
    # Clamp to max brightness
    total_brightness = min(1.0, total_brightness)
    
    if total_brightness > 0 and total_saturation > 0:
        # Render with color
        avg_hue = total_hue / total_saturation
        avg_saturation = min(1.0, total_saturation / total_brightness)
        return hsv(avg_hue, avg_saturation, total_brightness)
    else:
        # White/grayscale (or no light)
        return rgb(
            int(255 * total_brightness),
            int(255 * total_brightness),
            int(255 * total_brightness)
        )
