import customtkinter as ctk
import backend.utils as u


class LightboardKeyboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.buttons = {}
        self.create_keys()

    def create_keys(self):
        button_width = 20
        button_height = 20
        button_padx = 2
        button_pady = 2
        outer_padding = 5

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
                    state="disabled",
                    fg_color="gray20"
                )
                btn.place(x=x, y=y)
                self.buttons[letter] = btn

        # Ukupna širina/visina frame-a
        total_width = 2 * outer_padding + max_keys * button_width + (max_keys - 1) * button_padx
        total_height = 2 * outer_padding + row_count * button_height + (row_count - 1) * button_pady

        self.configure(width=total_width, height=total_height)

    def highlight_key(self, letter):
        self.reset_highlight()
        if letter is None:
            return
        btn = self.buttons.get(letter.upper())
        if btn:
            btn.configure(fg_color="yellow", text_color="black")
            self.after(500, self.reset_highlight)

    def reset_highlight(self):
        for btn in self.buttons.values():
            btn.configure(fg_color="gray20", text_color="white")
