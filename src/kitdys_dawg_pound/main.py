import pygame

from kitdys_dawg_pound.models.plinko_bins import PlinkoBins
from kitdys_dawg_pound.ui.popup import Popup
from kitdys_dawg_pound.ui.editor import PlinkoEditor
from kitdys_dawg_pound.models.plinko_ball import Ball  # Import the Ball class
from pyparsing import withClass


def run_game():
    # Initialize pygame
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Plinko Game")


    # Game state
    pin_rows = 6
    bin_texts = ["Empty Car","Remove Water", "Remove Food", "Pee off Roof", "Off Roading Only", "Walking Only", "Restart Game"]

    # Create bins
    bins = PlinkoBins(pin_rows, bin_texts)

    # Create editor
    editor = PlinkoEditor(width, height)
    editor.create_bin_textboxes(bin_texts)

    # Ball - start with no ball
    ball = None

    # Game loop variables
    clock = pygame.time.Clock()
    running = True

    popup = Popup()
    popup_font = pygame.font.SysFont("Gill Sans", 36)

    ratio = 1.0
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                ratio = event.size[0] / width
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                game_x = int(mouse_pos[0] / ratio)
                game_y = int(mouse_pos[1] / ratio)
                if popup.check_click(event.pos):
                    continue


        # Handle editor events
        editor_result = editor.handle_events(events)

        # Handle game actions based on editor results
        if editor_result["drop_ball"] and (ball is None or not ball.active):
            # Create a new ball only if no active ball exists
            ball = Ball(width // 2, 20)  # Start slightly below the top

        if editor_result["mode_changed"]:
            # Toggle between play and edit mode
            if editor.edit_mode:
                # Entering edit mode - clear any active ball
                ball = None
                pygame.display.set_caption("Plinko Game - Edit Mode")
            else:
                pygame.display.set_caption("Plinko Game")

        if editor_result["rows_changed"] or editor_result["labels_changed"]:
            # Always get labels first from editor (user input takes precedence)
            if editor_result["labels_changed"]:
                bin_texts = editor.get_bin_labels()

            # Then update rows and maintain user-edited labels
            if editor_result["rows_changed"]:
                pin_rows = editor.get_row_value()
                bins = PlinkoBins(pin_rows, bin_texts)
            else:
                bins = PlinkoBins(pin_rows, bin_texts)

            # Update UI to match current state
            editor.create_bin_textboxes(bin_texts)

        # Draw game elements
        screen.fill((0,0,0))

        # Update and draw pins
        pins_start_y = 50
        pin_spacing = min(width // (pin_rows + 2), 50)
        pin_radius = 5

        # Create pins in triangular formation
        pins = []
        for row in range(pin_rows):
            # Calculate how many pins in this row
            num_pins_in_row = row + 1

            # Center the row of pins
            row_width = num_pins_in_row * pin_spacing
            row_start_x = (width - row_width) // 2

            for col in range(num_pins_in_row):
                pin_x = row_start_x + col * pin_spacing
                pin_y = pins_start_y + row * pin_spacing
                pins.append((pin_x, pin_y))
                pygame.draw.circle(screen, (77, 0, 75), (pin_x, pin_y), pin_radius)


        # Update and draw ball if it exists
        if ball:
            bin_hit = ball.update(pin_rows, width, pin_spacing, pins_start_y)
            if bin_hit is not None:
                bins.register_hit(bin_hit)
                bin_text = bins.bin_texts[bin_hit]
                popup = Popup()
                popup.show(f"You landed in {bin_text}!", bins.rgb_gradient[bin_hit])
            ball.draw(screen)

        # Draw bins
        # Calculate how many bins needed (pin_rows + 1)
        num_bins = pin_rows + 1
        bin_row_width = num_bins * pin_spacing
        bin_start_x = (width - bin_row_width) // 2
        bins.draw_bins(width, screen, 1.0, pin_spacing, pins_start_y, bin_start_x)

        # Draw editor UI on top
        editor.draw(screen)
        popup.draw(screen, popup_font)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_game()