"""
Create the pins for the plinko board.
"""

def create_pins(ratio: float, pin_radius: int, pin_rows: int, pin_start: int, width: int) -> list:
    pins = []
    pin_spacing = int(40 * ratio)
    offset = pin_spacing // 2
    for row in range(1, pin_rows + 1):
        row_offset = offset if row % 2 == 0 else 0
        for col in range(-(row//2) - 1, (row -1) //2 + 2):
            x = width // 2 + col * pin_spacing + row_offset
            y = row * pin_spacing + pin_start
            pins.append((x,y))
    return pins
