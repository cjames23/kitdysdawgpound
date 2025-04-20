import pygame
import random
import math

from kitdys_dawg_pound.models.colors import Colors

class Ball:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_x = random.uniform(-0.5, 0.5)  # Small initial horizontal velocity
        self.velocity_y = 0
        self.gravity = 0.2
        self.elasticity = 0.6
        self.active = True
        self.color = (250, 1, 62)

    def update(self, pin_rows, width, pin_spacing, pins_start_y):
        if not self.active:
            return None

        # Apply gravity and update position
        self.velocity_y += self.gravity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check for wall collisions
        if self.x - self.radius < 0:
            self.x = self.radius
            self.velocity_x = -self.velocity_x * self.elasticity
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.velocity_x = -self.velocity_x * self.elasticity

        # Check for pin collisions
        for row in range(pin_rows):
            num_pins_in_row = row + 1
            row_width = num_pins_in_row * pin_spacing
            row_start_x = (width - row_width) // 2

            for col in range(num_pins_in_row):
                pin_x = row_start_x + col * pin_spacing
                pin_y = pins_start_y + row * pin_spacing

                # Simple collision detection
                distance = math.sqrt((self.x - pin_x)**2 + (self.y - pin_y)**2)
                if distance < self.radius + 5:  # 5 is pin radius
                    # Bounce off pin
                    angle = math.atan2(self.y - pin_y, self.x - pin_x)
                    self.velocity_x = math.cos(angle) * 2
                    self.velocity_y = abs(self.velocity_y) * self.elasticity

                    # Add some randomness
                    self.velocity_x += random.uniform(-0.3, 0.3)

        # Check if ball reached bottom (bins)
        bin_bottom = pins_start_y + pin_rows * pin_spacing + 50
        if self.y > bin_bottom:
            # Calculate which bin the ball landed in
            offset = (pin_spacing // 2) if pin_rows % 2 == 0 else 0
            bin_index = int((self.x - offset) / pin_spacing)

            # Clamp to valid range
            bin_index = max(0, min(bin_index, pin_rows))

            self.active = False
            return bin_index

        return None

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)