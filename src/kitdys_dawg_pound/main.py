import pygame

from kitdys_dawg_pound.models.plinko_bins import PlinkoBins
from kitdys_dawg_pound.ui.drawing import draw_text_box
from kitdys_dawg_pound.ui.popup import Popup
from kitdys_dawg_pound.ui.editor import PlinkoEditor
from kitdys_dawg_pound.models.plinko_ball import Ball

def run_game():
    # Initialize pygame
    pygame.init()

    # Base dimensions (design size)
    BASE_WIDTH, BASE_HEIGHT = 800, 600

    # Start with resizable window
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Plinko Game")

    # Create render surface at base resolution
    game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

    # Game state
    pin_rows = 6
    bin_texts = ["Empty Car","Remove Water", "Remove Food", "Pee off Roof", "Off Roading Only", "Walking Only", "Restart Game"]

    # Create bins
    bins = PlinkoBins(pin_rows, bin_texts)

    # Create editor
    editor = PlinkoEditor(BASE_WIDTH, BASE_HEIGHT)
    editor.create_bin_textboxes(bin_texts)

    # Ball - start with no ball
    ball = None

    # Game loop variables
    clock = pygame.time.Clock()
    running = True

    popup = Popup()
    popup_font = pygame.font.SysFont("Gill Sans", 36)

    while running:
        # Calculate letterboxing offsets and scale
        screen_width, screen_height = screen.get_size()
        scale_x = screen_width / BASE_WIDTH
        scale_y = screen_height / BASE_HEIGHT
        scale_factor = min(scale_x, scale_y)

        # Calculate positioning offsets (for letterboxing)
        scaled_width = int(BASE_WIDTH * scale_factor)
        scaled_height = int(BASE_HEIGHT * scale_factor)
        offset_x = (screen_width - scaled_width) // 2
        offset_y = (screen_height - scaled_height) // 2

        # Collect all mouse events for this frame
        events_to_process = []
        mouse_moved = False
        current_mouse_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                # Get screen mouse position
                screen_pos = event.pos

                # First check if the click is within the game area
                if (offset_x <= screen_pos[0] <= offset_x + scaled_width and
                        offset_y <= screen_pos[1] <= offset_y + scaled_height):

                    # Convert screen coordinates to game coordinates with offset
                    game_x = (screen_pos[0] - offset_x) / scale_factor
                    game_y = (screen_pos[1] - offset_y) / scale_factor
                    game_pos = (int(game_x), int(game_y))

                    if event.type == pygame.MOUSEMOTION:
                        mouse_moved = True
                        current_mouse_pos = game_pos

                    # Create event with proper coordinates
                    scaled_event = pygame.event.Event(event.type, {
                        'pos': game_pos,
                        'button': event.button if event.type == pygame.MOUSEBUTTONDOWN else 0
                    })

                    # Only check popup with scaled coordinates for MOUSEBUTTONDOWN
                    if event.type == pygame.MOUSEBUTTONDOWN and popup.check_click(game_pos):
                        continue  # Skip this event if popup handled it

                    events_to_process.append(scaled_event)
            else:
                events_to_process.append(event)

        # If mouse moved, always add a new motion event at the end to ensure hover states update
        if mouse_moved and current_mouse_pos:
            # Add an extra MOUSEMOTION event to ensure UI hover states are updated correctly
            events_to_process.append(pygame.event.Event(pygame.MOUSEMOTION, {
                'pos': current_mouse_pos,
                'buttons': pygame.mouse.get_pressed()
            }))

        # Handle editor events with converted positions
        editor_result = editor.handle_events(events_to_process)

        # Handle game actions based on editor results
        if editor_result["drop_ball"] and (ball is None or not ball.active):
            ball = Ball(BASE_WIDTH // 2, 20)

        if editor_result["mode_changed"]:
            if editor.edit_mode:
                ball = None
                pygame.display.set_caption("Plinko Game - Edit Mode")
            else:
                pygame.display.set_caption("Plinko Game")

        if editor_result["rows_changed"] or editor_result["labels_changed"]:
            if editor_result["labels_changed"]:
                bin_texts = editor.get_bin_labels()

            if editor_result["rows_changed"]:
                pin_rows = editor.get_row_value()
                bins = PlinkoBins(pin_rows, bin_texts)
            else:
                bins = PlinkoBins(pin_rows, bin_texts)

            editor.create_bin_textboxes(bin_texts)

        # Clear the game surface
        game_surface.fill((195, 177, 225))

        text_message = "Kitdy's Dawg Pound"  # Change this to whatever text you need
        draw_text_box(game_surface, text_message, 20, 20, 24,bg_color=(195, 177, 225),text_color=(128, 0, 128), ratio=1.0)

        # Draw pins
        pins_start_y = 50
        pin_spacing = min(BASE_WIDTH // (pin_rows + 2), 50)
        pin_radius = 5

        # Create pins in triangular formation
        pins = []
        for row in range(pin_rows):
            num_pins_in_row = row + 1
            row_width = num_pins_in_row * pin_spacing
            row_start_x = (BASE_WIDTH - row_width) // 2

            for col in range(num_pins_in_row):
                pin_x = row_start_x + col * pin_spacing
                pin_y = pins_start_y + row * pin_spacing
                pins.append((pin_x, pin_y))
                pygame.draw.circle(game_surface,  (159, 43, 104),(pin_x, pin_y), pin_radius)


        # Update and draw ball if it exists
        # Update and draw ball if it exists
        if ball:
            bin_hit = ball.update(pin_rows, BASE_WIDTH, pin_spacing, pins_start_y)

            # Calculate where the bottom of the bins should be
            bin_bottom_y = pins_start_y + (pin_rows * pin_spacing) + 50  # Add extra space for bin height

            # Check if the ball has hit a bin or fallen below the bins
            if bin_hit is not None:
                # Ball hit a bin normally
                bins.register_hit(bin_hit)
                bin_text = bins.bin_texts[bin_hit]
                popup = Popup()
                popup.show(f"You landed in {bin_text}!", bins.rgb_gradient[bin_hit])
                ball = None  # Make ball disappear
            elif ball.y > bin_bottom_y:
                # Ball has fallen below the bins without registering a hit
                # Find the closest bin based on x-position
                num_bins = pin_rows + 1
                bin_width = pin_spacing
                bin_start_x = (BASE_WIDTH - (num_bins * bin_width)) // 2

                for i in range(num_bins):
                    bin_left = bin_start_x + (i * bin_width)
                    bin_right = bin_left + bin_width

                    if bin_left <= ball.x <= bin_right:
                        bins.register_hit(i)
                        bin_text = bins.bin_texts[i]
                        popup = Popup()
                        popup.show(f"You landed in {bin_text}!", bins.rgb_gradient[i])
                        break

                ball = None  # Make ball disappear
            else:
                ball.draw(game_surface)  # Only draw if ball is still active

        # Draw bins - pass the actual scale_factor instead of 1.0
        num_bins = pin_rows + 1
        bin_row_width = num_bins * pin_spacing
        bin_start_x = (BASE_WIDTH - bin_row_width) // 2
        bins.draw_bins(BASE_WIDTH, game_surface, scale_factor, pin_spacing, pins_start_y, bin_start_x)

        # Draw editor UI and popup
        editor.draw(game_surface)
        popup.draw(game_surface, popup_font)

        # First fill the screen with black (for letterboxing)
        screen.fill((195, 177, 225))

        # Scale game surface while maintaining aspect ratio
        scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_width, scaled_height))

        # Blit the scaled surface at the correct position
        screen.blit(scaled_surface, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_game()