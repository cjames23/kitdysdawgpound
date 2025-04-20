from kitdys_dawg_pound.models.colors import Colors, create_rgb_gradient


def create_plinko_gradients(pin_rows):
    """Create color gradients for plinko bins.

    Args:
        pin_rows: Number of pin rows

    Returns:
        Tuple of (rgb_gradient, dark_rgb_gradient)
    """
    # Create main gradient from red to yellow
    rgb_gradient = create_rgb_gradient(Colors.RED.value, Colors.YELLOW.value, (pin_rows+2) // 2)
    rgb_gradient_rev = rgb_gradient[::-1]
    rgb_gradient.extend(rgb_gradient_rev[1:])

    # Create darker gradient for shadows
    dark_rgb_gradient = create_rgb_gradient(Colors.DARK_RED.value, Colors.DARK_YELLOW.value, (pin_rows+2) // 2)
    dark_rgb_gradient_rev = dark_rgb_gradient[::-1]
    dark_rgb_gradient.extend(dark_rgb_gradient_rev[1:])

    return rgb_gradient, dark_rgb_gradient
