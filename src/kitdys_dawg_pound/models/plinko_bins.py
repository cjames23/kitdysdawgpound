import pygame

from kitdys_dawg_pound.ui.drawing import draw_rounded_rect
from kitdys_dawg_pound.ui.gradient import create_plinko_gradients
from kitdys_dawg_pound.ui.text import create_bin_texts


class PlinkoBins:
    def __init__(self, pin_rows, bin_texts):
        """Initialize plinko bins manager.

        Args:
            pin_rows: Number of pin rows
            bin_texts: List of text labels for bins
        """
        self.pin_rows = pin_rows
        self.bin_texts = bin_texts
        self.hit_bins = []
        self.rgb_gradient, self.dark_rgb_gradient = create_plinko_gradients(pin_rows)

        # Store indices of recent bins
        recent_start = 8 - pin_rows // 2
        self.recent_bins = bin_texts[recent_start:recent_start+4]
        self.recent_bin_colors = self.rgb_gradient[recent_start:recent_start+4]

    def draw_bins(self, width, screen, ratio, pin_spacing, pins_start_y, pins_start_x=0):
        """Draw all bins on the screen."""
        bin_width = (pin_spacing * 0.8)
        click_offset = 4 * ratio

        # Calculate bottom row pin positions
        bottom_row = self.pin_rows - 1
        num_pins_in_bottom_row = bottom_row + 1
        row_width = num_pins_in_bottom_row * pin_spacing
        row_start_x = (width - row_width) // 2
        base_y = self.pin_rows * pin_spacing + pins_start_y + pin_spacing // 2

        # Determine maximum possible font size first
        test_font = pygame.font.SysFont("Gill Sans", 36)
        max_text_width = 0
        for text in self.bin_texts:
            text_width = test_font.size(text)[0]
            max_text_width = max(max_text_width, text_width)

        # Calculate scaling factor based on actual text width
        scaling_factor = bin_width / (max_text_width + 10)  # Add padding
        font_size = int(36 * scaling_factor * ratio)

        # Ensure minimum and maximum size
        font_size = max(10, min(36, font_size))

        # Create font object instead of pre-rendered surfaces
        font = pygame.font.SysFont("Gill Sans", font_size)

        # Position and draw each bin
        for bin_index in range(self.pin_rows + 1):
            bin_x = row_start_x + (bin_index * pin_spacing) - (pin_spacing / 2)
            self._draw_single_bin(
                screen, bin_index, base_y, bin_x, bin_width,
                pin_spacing, font, click_offset, ratio
            )

    def _draw_single_bin(
            self,
            screen,
            bin_index,
            base_y,
            bin_x,
            bin_width,
            pin_spacing,
            font,
            click_offset,
            ratio,
    ):
        animate = bin_index in self.hit_bins
        base_x = bin_x - bin_width // 2
        corner_radius = int(4 * ratio) + (ratio > 1)
        bin_height = bin_width  # Square bin

        # Set orange color for bins
        bin_color = (255, 165, 0)  # Orange
        shadow_color = (200, 120, 0)  # Darker orange for shadow

        if animate:
            light_rect = pygame.Rect(base_x, base_y + click_offset, bin_width, bin_height)
            # Draw orange rectangle
            draw_rounded_rect(screen, light_rect, bin_color, corner_radius)

            # Wrap and draw black text
            self._draw_wrapped_text(
                screen, font, self.bin_texts[bin_index],
                (0, 0, 0),  # Black text
                base_x, base_y + click_offset, bin_width, bin_height
            )

            # Remove from hit bins after drawing
            self.hit_bins = list(filter(lambda x: x != bin_index, self.hit_bins))
        else:
            dark_rect = pygame.Rect(base_x, base_y + click_offset, bin_width, bin_height)
            light_rect = pygame.Rect(base_x, base_y, bin_width, bin_height)

            # Draw shadow and orange rectangle
            draw_rounded_rect(screen, dark_rect, shadow_color, corner_radius)
            draw_rounded_rect(screen, light_rect, bin_color, corner_radius)

            # Wrap and draw black text
            self._draw_wrapped_text(
                screen, font, self.bin_texts[bin_index],
                (0, 0, 0),  # Black text
                base_x, base_y, bin_width, bin_height
            )

    def _draw_wrapped_text(self, screen, font, text, color, x, y, width, height):
        """Draw text wrapped within the given rectangle."""
        words = text.split(' ')
        lines = []
        current_line = []

        # Create wrapped lines
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]

            if test_width <= width - 10:  # 5px padding on each side
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        # Render text lines
        line_height = font.get_linesize()
        total_height = line_height * len(lines)
        start_y = y + (height - total_height) // 2

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(
                center=(x + width // 2, start_y + i * line_height + line_height // 2)
            )
            screen.blit(text_surface, text_rect)

    def register_hit(self, bin_index):
        """Register a bin as being hit by a ball.

        Args:
            bin_index: Index of the bin that was hit
        """
        if bin_index not in self.hit_bins:
            self.hit_bins.append(bin_index)

    def update_pin_rows(self, new_rows):
        """Update the number of pin rows and adjust bin texts accordingly.

        Args:
            new_rows: New number of pin rows
        """
        self.pin_rows = new_rows

        # Ensure we have the correct number of bin texts (should be pin_rows + 1)
        needed_bins = new_rows + 1
        if len(self.bin_texts) != needed_bins:
            # Generate new bin texts if the count doesn't match
            template = ["$1", "$5", "$10", "$25", "$50", "$25", "$10", "$5", "$1"]

            # If we need fewer bins than template, take from the middle
            if needed_bins <= len(template):
                start_idx = (len(template) - needed_bins) // 2
                self.bin_texts = template[start_idx:start_idx + needed_bins]
            else:
                # If we need more, duplicate values to reach the required count
                self.bin_texts = []
                for i in range(needed_bins):
                    self.bin_texts.append(template[i % len(template)])

        # Regenerate color gradients
        self.rgb_gradient, self.dark_rgb_gradient = create_plinko_gradients(new_rows)

        # Update recent bins info
        recent_start = min(8 - new_rows // 2, max(0, len(self.bin_texts) - 4))
        end_idx = min(recent_start + 4, len(self.bin_texts))
        self.recent_bins = self.bin_texts[recent_start:end_idx]
        self.recent_bin_colors = self.rgb_gradient[recent_start:end_idx]
