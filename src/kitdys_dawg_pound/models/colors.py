from enum import Enum

def convert_color(rgb_color):
    return tuple([x / 255 for x in rgb_color])


class Colors(Enum):
    """Enum for managing colors in the game."""
    BACKGROUND = convert_color((19, 33, 45))
    RED = (250, 1, 62)
    YELLOW = convert_color((252, 192, 2))
    DARK_RED = convert_color((146, 0, 7))
    DARK_YELLOW = convert_color((155, 120, 0))
    WHITE = (1.0, 1.0, 1.0)
    GRAY = (0.5, 0.5, 0.5)
    OPAQUE_WHITE = (1.0, 1.0, 1.0, 0.588)
    BLACK = (0.0, 0.0, 0.0)
    GREEN = convert_color((32, 250, 32))
    HOVER_GREEN = (24 / 255, 200 / 255, 24 / 255)
    DARK_GREEN = (16 / 255, 150 / 255, 16 / 255)
    BUTTON_COLOR_STATES = (GREEN, HOVER_GREEN, DARK_GREEN)


def create_rgb_gradient(start_color, end_color, steps):
    """Generate a list of RGB colors forming a gradient between two given RGB colors."""
    # Calculate the difference per step
    step_red = (end_color[0] - start_color[0]) / (steps - 1)
    step_green = (end_color[1] - start_color[1]) / (steps - 1)
    step_blue = (end_color[2] - start_color[2]) / (steps - 1)

    # Generate the gradient list
    gradient = [
        (
            int(start_color[0] + step_red * i),
            int(start_color[1] + step_green * i),
            int(start_color[2] + step_blue * i)
        )
        for i in range(steps)
    ]
    return gradient
