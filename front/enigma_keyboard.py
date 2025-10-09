import customtkinter as ctk
import backend.utils as u


class EnigmaKeyboard(ctk.CTkFrame):
    def __init__(self, master, on_key_press, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_key_press = on_key_press
        self.create_keyboard()

    def create_keyboard(self):
        button_width = 40
        button_height = 40
        button_padx = 5
        button_pady = 5
        outer_padding = 20

        max_keys = max(len(row) for row in u.KEYBOARD_LAYOUT)
        row_count = len(u.KEYBOARD_LAYOUT)

        middle_row_offset = (button_width + button_padx) // 2

        for row_id, row_keys in enumerate(u.KEYBOARD_LAYOUT):
            y = outer_padding + row_id * (button_height + button_pady)

            offset_x = 0
            if row_id == 1:
                offset_x = middle_row_offset

            for i, letter in enumerate(row_keys):
                # Pomeri x poziciju za outer_padding + offset
                x = outer_padding + offset_x + i * (button_width + button_padx)

                btn = ctk.CTkButton(
                    self,
                    text=letter,
                    width=button_width,
                    height=button_height,
                    command=lambda ll=letter: self.handle_press(ll)
                )
                btn.place(x=x, y=y)

        # Ukupna širina/visina frame-a
        total_width = 2 * outer_padding + max_keys * button_width + (max_keys - 1) * button_padx
        total_height = 2 * outer_padding + row_count * button_height + (row_count - 1) * button_pady

        self.configure(width=total_width, height=total_height)

    def handle_press(self, letter):
        self.on_key_press(letter.upper())
