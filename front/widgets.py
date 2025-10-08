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
            label = ctk.CTkLabel(self, text="", width=50, height=50, corner_radius=8,
                                 fg_color="black", font=("Arial", 30))
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
                lbl.configure(font=("Arial", 28, "bold"))
            else:
                lbl.configure(font=("Arial", 24))

            # Oboji ako je trenutni karakter notch
            if char in self.notch:
                lbl.configure(fg_color="#456eba")  # plava za notch
            else:
                lbl.configure(fg_color="#001d4d")


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
        outer_padding = 20  # <-- dodaj ovo za prostor oko cele tastature

        max_keys = max(len(row) for row in KEYBOARD_LAYOUT)
        row_count = len(KEYBOARD_LAYOUT)

        middle_row_offset = (button_width + button_padx) // 2

        for row_id, row_keys in enumerate(KEYBOARD_LAYOUT):
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


class PlugboardWidget(ctk.CTkFrame):
    PAIR_COLORS = [
        "#FF6B6B",  # crvena
        "#6BCB77",  # zelena
        "#4D96FF",  # plava
        "#FFD93D",  # zuta
        "#9D4EDD",  # ljubicasta
        "#FF924C",  # narandzasta
        "#3AB0FF",  # svetloplava
        "#A8DF8E",  # mint
        "#FF5DA2",  # pink
        "#00C49A"   # teal
    ]

    def __init__(self, master, on_update=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_update = on_update
        self.letter_buttons = {}
        self.plugboard_connections = []
        self.selected_letter = None
        self.pair_color_map = {}

        self.create_widgets()

    def create_widgets(self):
        layout_frame = ctk.CTkFrame(self)
        layout_frame.pack(padx=10, pady=10, fill="x")
        half = (len(u.ALPHABET) - 1) // 2
        # Dugmici za slova
        for i, letter in enumerate(u.ALPHABET):
            btn = ctk.CTkButton(
                layout_frame,
                text=letter,
                width=30,
                height=30,
                font=("Arial", 12),
                command=lambda ll=letter: self.on_letter_click(ll)
            )
            if i < 13:
                btn.grid(row=0, column=i, padx=2, pady=2)
            else:
                btn.grid(row=1, column=i-13, padx=2, pady=2)
            self.letter_buttons[letter] = btn

    def get_connections(self):
        return self.plugboard_connections.copy()

    def remove_last_connection(self):
        if self.plugboard_connections:
            last = self.plugboard_connections.pop()
            self.pair_color_map.pop(last, None)
            self.selected_letter = None
            self.update_display()
            if self.on_update:
                self.on_update(self.plugboard_connections)

    def clear_all_connections(self):
        self.plugboard_connections.clear()
        self.pair_color_map.clear()
        self.selected_letter = None
        self.update_display()
        if self.on_update:
            self.on_update(self.plugboard_connections)

    # ostalo isto

    def _is_connected(self, letter):
        return any(letter in pair for pair in self.plugboard_connections)

    def on_letter_click(self, letter):
        # Ako je slovo povezano, ne radi nista
        if self._is_connected(letter):
            return

        if len(self.plugboard_connections) >= 10:
            return

        # Selektuj / Deselektuj
        if self.selected_letter == letter:
            self.selected_letter = None
        else:
            if self.selected_letter is not None:
                pair = tuple(sorted([self.selected_letter, letter]))
                if pair not in self.plugboard_connections:
                    self.plugboard_connections.append(pair)
                    # Boja
                    if len(self.plugboard_connections) <= len(self.PAIR_COLORS):
                        self.pair_color_map[pair] = self.PAIR_COLORS[len(self.plugboard_connections) - 1]
                self.selected_letter = None
            else:
                self.selected_letter = letter

        self.update_display()
        if self.on_update:
            self.on_update(self.plugboard_connections)

    def update_display(self):
        # Prvo reset
        for letter, btn in self.letter_buttons.items():
            btn.configure(fg_color="gray20", text_color="white")

        # Bojenje parova
        for pair in self.plugboard_connections:
            color = self.pair_color_map.get(pair, "gray50")
            for ll in pair:
                self.letter_buttons[ll].configure(fg_color=color, text_color="white")

        if self.selected_letter:
            self.letter_buttons[self.selected_letter].configure(fg_color="#22CC88", text_color="white")
