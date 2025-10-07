import customtkinter as ctk
import backend.utils as u

class SpinnerSelector(ctk.CTkFrame):
    def __init__(self, master, initial=0, mode="number", **kwargs):
        super().__init__(master, **kwargs)
        self.mode = mode.lower()

        if self.mode == "letter":
            if isinstance(initial, str):
                self.value = (ord(initial.upper()) - u.ORD_A) % u.ALPHABET_NUM
            else:
                self.value = int(initial) % u.ALPHABET_NUM
        else:
            self.value = int(initial) % 26

        self.label = ctk.CTkLabel(self, text=self.display_value(), width=40)
        self.label.grid(row=0, column=1, padx=5)

        self.minus_button = ctk.CTkButton(self, text="-", width=30, command=self.decrease)
        self.minus_button.grid(row=0, column=0)

        self.plus_button = ctk.CTkButton(self, text="+", width=30, command=self.increase)
        self.plus_button.grid(row=0, column=2)

    def display_value(self):
        return chr(self.value + ord('A')) if self.mode == "letter" else str(self.value)

    def increase(self):
        self.value = (self.value + 1) % u.ALPHABET_NUM
        self.label.configure(text=self.display_value())

    def decrease(self):
        self.value = (self.value - 1) % u.ALPHABET_NUM
        self.label.configure(text=self.display_value())

    def get(self):
        return chr(self.value + u.ORD_A) if self.mode == "letter" else self.value

    def set(self, val):
        if self.mode == "letter":
            if isinstance(val, str):
                self.value = (ord(val.upper()) - u.ORD_A) % u.ALPHABET_NUM
            else:
                self.value = int(val) % u.ALPHABET_NUM
        else:
            self.value = int(val) % u.ALPHABET_NUM
        self.label.configure(text=self.display_value())


class RotorDisplay(ctk.CTkFrame):
    def __init__(self, master, rotor_wiring, notch, position_char="A", **kwargs):
        super().__init__(master, **kwargs)
        self.rotor_wiring = rotor_wiring
        self.notch = notch
        self.position = ord(position_char.upper()) - u.ORD_A

        self.cells = []
        self.create_display()

    def create_display(self):
        for i in range(5):
            label = ctk.CTkLabel(self, text="", width=40, height=40, corner_radius=8,
                                 fg_color="gray20", font=("Arial", 20))
            label.grid(row=i, column=0, pady=2)
            self.cells.append(label)

        self.update_display()

    def update_display(self, position_char=None):
        if position_char is not None:
            self.position = ord(position_char.upper()) - u.ORD_A

        for i, offset in enumerate([-2, -1, 0, 1, 2]):
            pos = (self.position + offset) % u.ALPHABET_NUM
            char = u.ALPHABET[pos]

            lbl = self.cells[i]
            lbl.configure(text=char)

            # Trenutni (centralni) red
            if i == 2:
                lbl.configure(font=("Arial", 24, "bold"))
            else:
                lbl.configure(font=("Arial", 20))

            # Oboji ako je trenutni karakter notch
            if char in self.notch:
                lbl.configure(fg_color="#3a7bd5")  # plava za notch
            else:
                lbl.configure(fg_color="gray20")


KEYBOARD_LAYOUT = [
    list("QWERTZUIO"),
    list("ASDFGHJK"),
    list("PYXCVBNML")
]
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

        max_keys = max(len(row) for row in KEYBOARD_LAYOUT)
        total_width = max_keys * (button_width + 2*button_padx)

        middle_row_offset = (button_width + 2*button_padx) // 2

        for row_id, row_keys in enumerate(KEYBOARD_LAYOUT):
            y = row_id * (button_height + 2*button_pady)

            offset_x = 0
            if row_id == 1:
                offset_x = middle_row_offset

            for i, letter in enumerate(row_keys):
                x = offset_x + i * (button_width + 2 * button_padx)
                btn = ctk.CTkButton(
                    self,
                    text=letter,
                    width=button_width,
                    height=button_height,
                    command=lambda ll=letter: self.handle_press(ll)
                )
                btn.place(x=x,y=y)

        total_height = len(KEYBOARD_LAYOUT) * (button_height + 2 * button_pady)
        self.configure(width=total_width, height=total_height)

    def handle_press(self, letter):
        self.on_key_press(letter.upper())
