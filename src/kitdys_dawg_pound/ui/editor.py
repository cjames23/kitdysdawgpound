import pygame

from kitdys_dawg_pound.ui.ui_controls import Button, TextBox


class PlinkoEditor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.edit_mode = False

        # Create UI elements
        self.row_label = pygame.font.SysFont("Arial", 24).render("Number of Rows:", True, (255, 255, 255))
        self.row_textbox = TextBox(180, 20, 60, 40, "8")

        # Create buttons
        self.edit_button = Button(width - 120, 20, 100, 40, "Edit")
        self.play_button = Button(width - 230, 20, 100, 40, "Play")
        self.apply_button = Button(width - 120, height - 60, 100, 40, "Apply")

        # Bin label textboxes (created dynamically)
        self.bin_textboxes = []
        self.update_bin_textboxes(self.get_row_value())

    def create_bin_textboxes(self, bin_texts):
        self.bin_textboxes = []
        y_pos = 80
        for i, text in enumerate(bin_texts):
            textbox = TextBox(20, y_pos + i * 50, 150, 40, text)
            self.bin_textboxes.append(textbox)

    def handle_events(self, events):
        result = {"mode_changed": False, "rows_changed": False, "labels_changed": False, "drop_ball": False}

        for event in events:
            # Handle mode buttons
            if self.edit_button.handle_event(event) and not self.edit_mode:
                self.edit_mode = True
                result["mode_changed"] = True

            # If in edit mode, clicking play exits edit mode
            # If already in play mode, clicking play drops a ball
            if self.play_button.handle_event(event):
                if self.edit_mode:
                    self.edit_mode = False
                    result["mode_changed"] = True
                else:
                    # Signal to drop a ball when in play mode
                    result["drop_ball"] = True

            # In edit mode, handle apply button
            if self.edit_mode and self.apply_button.handle_event(event):
                # Validate and apply changes
                try:
                    # Check if row value changed
                    old_row_value = len(self.bin_textboxes) - 1  # Bins = rows + 1
                    new_row_value = self.get_row_value()

                    if new_row_value != old_row_value:
                        result["rows_changed"] = True
                        # Update bin textboxes to match the new row count
                        self.update_bin_textboxes(new_row_value)
                except ValueError:
                    pass

                # Get bin labels
                bin_labels = self.get_bin_labels()
                result["labels_changed"] = True
                self.edit_mode = False

            # In edit mode, handle other controls
            if self.edit_mode:
                self.row_textbox.handle_event(event)
                for textbox in self.bin_textboxes:
                    textbox.handle_event(event)

        return result

    def draw(self, screen):
        # Always draw mode buttons
        self.edit_button.draw(screen)
        self.play_button.draw(screen)

        if self.edit_mode:
            # Draw editor UI
            pygame.draw.rect(screen, (40, 40, 40, 200), (0, 0, self.width, self.height))

            # Draw row controls
            screen.blit(self.row_label, (20, 30))
            self.row_textbox.draw(screen)

            # Draw bin label section
            bin_title = pygame.font.SysFont("Arial", 24).render("Bin Labels:", True, (255, 255, 255))
            screen.blit(bin_title, (20, 80 - 30))

            for textbox in self.bin_textboxes:
                textbox.draw(screen)

            self.apply_button.draw(screen)

    def get_row_value(self):
        try:
            return max(2, min(15, int(self.row_textbox.text)))
        except ValueError:
            return 8

    def get_bin_labels(self):
        return [textbox.text for textbox in self.bin_textboxes]

    def update_bin_textboxes(self, rows):
        # Calculate bin count (rows + 1)
        bin_count = rows + 1

        # Get current bin labels or create defaults
        current_labels = self.get_bin_labels() if self.bin_textboxes else []

        # Create default labels for any new bins
        while len(current_labels) < bin_count:
            current_labels.append(f"Bin {len(current_labels)}")

        # Trim if we have too many
        if len(current_labels) > bin_count:
            current_labels = current_labels[:bin_count]

        # Recreate textboxes with updated labels
        self.create_bin_textboxes(current_labels)
