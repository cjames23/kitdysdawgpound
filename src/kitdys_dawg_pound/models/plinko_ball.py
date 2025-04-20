import pygame
import random
import math

class Ball:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_x = random.uniform(-0.15, 0.15)
        self.velocity_y = 0
        self.gravity = 0.2
        self.elasticity = 0.65
        self.active = True
        self.color = (112, 41, 99)
        self.last_collision_time = 0

    def update(self, pin_rows, width, pin_spacing, pins_start_y):
        if not self.active:
            return None

        # Apply gravity
        self.velocity_y += self.gravity

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collisions
        if self.x - self.radius < 0:
            self.x = self.radius
            self.velocity_x = -self.velocity_x * self.elasticity
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.velocity_x = -self.velocity_x * self.elasticity

        # Check pin collisions using the same logic from create_pins function
        pin_radius = 5
        offset = pin_spacing // 2

        # This exactly matches the create_pins logic
        for row in range(1, pin_rows + 1):
            row_offset = offset if row % 2 == 0 else 0
            for col in range(-(row//2) - 1, (row-1)//2 + 2):
                pin_x = width // 2 + col * pin_spacing + row_offset
                pin_y = row * pin_spacing + pins_start_y

                if self.check_pin_collision(pin_x, pin_y, pin_radius, width, pin_spacing):
                    pass  # Continue checking other pins

        # Check if ball reached bottom (bins)
        bin_bottom = pins_start_y + pin_rows * pin_spacing + 100
        if self.y > bin_bottom:
            # Calculate which bin the ball landed in
            num_bins = pin_rows + 1

            # Calculate bin index based on the same pin spacing logic
            bottom_row_width = num_bins * pin_spacing
            bottom_row_start_x = (width - bottom_row_width) / 2
            bin_index = int((self.x - bottom_row_start_x) / pin_spacing)

            # Ensure bin_index is within valid range
            bin_index = max(0, min(bin_index, num_bins - 1))

            self.active = False
            return bin_index

        return None

    def check_pin_collision(self, pin_x, pin_y, pin_radius, width, pin_spacing):
        # Calculate distance between ball and pin
        dx = self.x - pin_x
        dy = self.y - pin_y
        dist_sq = dx * dx + dy * dy
        radius_sum = self.radius + pin_radius

        # Collision detected
        if dist_sq < radius_sum * radius_sum:
            # Prevent multiple collisions in same frame
            current_time = pygame.time.get_ticks()
            if current_time - self.last_collision_time < 50:  # 50ms cooldown
                return False

            self.last_collision_time = current_time

            # Calculate overlap and angle
            overlap = radius_sum - math.sqrt(dist_sq)
            angle = math.atan2(dy, dx)

            # Move ball outside pin to prevent sticking/tunneling
            displacement = overlap + 0.5  # Extra 0.5 pixels to ensure separation
            self.x += math.cos(angle) * displacement
            self.y += math.sin(angle) * displacement

            # Calculate normal vector for reflection
            normal_x = math.cos(angle)
            normal_y = math.sin(angle)

            # Calculate dot product and reflection
            dot_product = self.velocity_x * normal_x + self.velocity_y * normal_y
            self.velocity_x = self.velocity_x - 2 * dot_product * normal_x
            self.velocity_y = self.velocity_y - 2 * dot_product * normal_y

            # Apply elasticity and dampening
            self.velocity_x *= self.elasticity * 0.5
            self.velocity_y *= self.elasticity

            # Add center bias after collision
            center_x = width / 2
            if self.x > center_x + pin_spacing:
                self.velocity_x -= 0.05  # Push left if on the right side
            elif self.x < center_x - pin_spacing:
                self.velocity_x += 0.05  # Push right if on the left side

            # Random bias toward center (70% chance)
            if random.random() < 0.7:
                bias_direction = 1 if self.x < center_x else -1
                self.velocity_x += bias_direction * 0.02

            return True
        return False

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)