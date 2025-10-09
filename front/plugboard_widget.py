import customtkinter as ctk
import backend.utils as u


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
        "#00C49A"  # teal
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
                btn.grid(row=1, column=i - 13, padx=2, pady=2)
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
