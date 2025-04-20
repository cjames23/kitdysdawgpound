import pygame


def draw_rounded_rect(surface, rect, color, corner_radius, corners=[True, True, True, True]):
    """Draw a rectangle with selectable rounded or square corners on the given surface."""
    top_left, top_right, bottom_left, bottom_right = corners

    # Central rectangle
    central_rect = pygame.Rect(rect.x + corner_radius, rect.y + corner_radius,
                               rect.width - 2 * corner_radius, rect.height - 2 * corner_radius)
    pygame.draw.rect(surface, color, central_rect)

    # Horizontal and vertical bars
    horizontal_rect = pygame.Rect(rect.x + corner_radius, rect.y,
                                  rect.width - 2 * corner_radius, rect.height)
    vertical_rect = pygame.Rect(rect.x, rect.y + corner_radius,
                                rect.width, rect.height - 2 * corner_radius)
    pygame.draw.rect(surface, color, horizontal_rect)
    pygame.draw.rect(surface, color, vertical_rect)

    # Draw corners
    if top_left:
        pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.top + corner_radius), corner_radius)
    else:
        pygame.draw.rect(surface, color, (rect.left, rect.top, corner_radius, corner_radius))

    if top_right:
        pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.top + corner_radius), corner_radius)
    else:
        pygame.draw.rect(surface, color, (rect.right - corner_radius, rect.top, corner_radius, corner_radius))

    if bottom_left:
        pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.bottom - corner_radius), corner_radius)
    else:
        pygame.draw.rect(surface, color, (rect.left, rect.bottom - corner_radius, corner_radius, corner_radius))

    if bottom_right:
        pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.bottom - corner_radius), corner_radius)
    else:
        pygame.draw.rect(surface, color, (rect.right - corner_radius, rect.bottom - corner_radius, corner_radius, corner_radius))
