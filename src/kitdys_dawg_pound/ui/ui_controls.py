import pygame


class TextBox:
    def __init__(self, x, y, width, height, text='', active_color=(0, 200, 255),
                 inactive_color=(100, 100, 100), text_color=(255, 255, 255), font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size)
        self.active = False
        self.rendered_text = self.font.render(self.text, True, self.text_color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True  # Value was submitted
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

            self.rendered_text = self.font.render(self.text, True, self.text_color)
        return False

    def draw(self, screen):
        color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, color, self.rect, 2)

        text_rect = self.rendered_text.get_rect(center=self.rect.center)
        screen.blit(self.rendered_text, text_rect)

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 200),
                 hover_color=(150, 150, 255), text_color=(255, 255, 255), font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size)
        self.rendered_text = self.font.render(self.text, True, self.text_color)

    def check_hover(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.check_hover(event.pos):
                return True
        return False

    def draw(self, screen):
        color = self.hover_color if self.check_hover(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect)

        text_rect = self.rendered_text.get_rect(center=self.rect.center)
        screen.blit(self.rendered_text, text_rect)
