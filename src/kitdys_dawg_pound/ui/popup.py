import pygame

from kitdys_dawg_pound.ui.drawing import draw_rounded_rect


class Popup:
    def __init__(self):
        self.active = False
        self.message = ""
        self.color = (255, 255, 255)
        self.rect = None
        self.min_width = 200
        self.min_height = 80
        self.padding = 20

    def show(self, message, color=None):
        self.active = True
        self.message = message
        if color:
            self.color = color

    def hide(self):
        self.active = False

    def check_click(self, pos):
        """Check if popup was clicked and hide it if so."""
        if self.active and self.rect and self.rect.collidepoint(pos):
            self.hide()
            return True
        return False

    def draw(self, screen, font):
        if not self.active:
            return

        # First measure the text to determine popup size
        text_width, text_height = font.size(self.message)

        # Calculate popup dimensions based on text
        popup_width = max(self.min_width, text_width + self.padding * 2)
        popup_height = max(self.min_height, text_height + self.padding * 2)

        # Center the popup
        width, height = screen.get_size()
        x = (width - popup_width) // 2
        y = height // 3

        # Store the popup rectangle for click detection
        self.rect = pygame.Rect(x, y, popup_width, popup_height)

        # Draw rounded rectangle with green background
        s = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        draw_rounded_rect(s, pygame.Rect(0, 0, popup_width, popup_height),
                          (128, 0, 128), 15)  # Green background

        # Draw black text regardless of self.color
        text = font.render(self.message, True, (195, 177, 225))  # Black text
        text_rect = text.get_rect(center=(popup_width//2, popup_height//2))
        s.blit(text, text_rect)

        # Draw to screen
        screen.blit(s, (x, y))