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
    def __init__(self, master, rotor_object, rotor_wiring, notch, position_char="A", **kwargs):
        super().__init__(master, **kwargs)
        self.rotor_object = rotor_object
        self.rotor_wiring = rotor_wiring
        self.notch = notch
        self.position = ord(position_char.upper()) - u.ORD_A
        self.button = None
        self.cells = []
        self.create_display()

    def create_display(self):
        for i in range(5):
            label = ctk.CTkLabel(self, text="", width=50, height=50, corner_radius=8,
                                 fg_color="black", font=("Arial", 30))
            label.grid(row=i, column=0, pady=2)
            self.cells.append(label)

        self.button = ctk.CTkButton(self, text="Nazad", command=self.rotate_backward)
        self.button.grid(row=5, column=0, pady=(10, 0))
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

    def rotate_backward(self):
        self.position = (self.position - 1) % u.ALPHABET_NUM
        self.update_display()

        if hasattr(self, "rotor_object"):
            self.rotor_object.undo_step()
