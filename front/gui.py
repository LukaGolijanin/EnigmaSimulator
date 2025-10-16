# import ctypes

import customtkinter as ctk
from backend.enigma_machine import EnigmaMachine
from backend.rotor import Rotor
from backend.reflector import Reflector
from backend.plugboard import Plugboard
import backend.utils as u
from front.widgets import SpinnerSelector, RotorDisplay
from front.plugboard_widget import PlugboardWidget
from front.enigma_keyboard import EnigmaKeyboard
from front.visualizer import EnigmaVisualizer
from front.lightboard_keyboard import LightboardKeyboard

ROTOR_NAMES = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
REFLECTOR_NAMES = ["R_A", "R_B", "R_C"]
POSITIONS = [chr(i) for i in range(u.ORD_A, ord('Z') + 1)]
RING_SETTINGS = list(range(26))


def get_reflector_wiring(name):
    if name == "R_A":
        return u.A_REFLECTOR
    elif name == "R_B":
        return u.B_REFLECTOR
    elif name == "R_C":
        return u.C_REFLECTOR
    else:
        raise ValueError("Nepostojeći reflektor!")


def get_wiring_for_name(param):
    if param == "I":
        return u.EnigmaI
    elif param == "II":
        return u.EnigmaII
    elif param == "III":
        return u.EnigmaIII
    elif param == "IV":
        return u.M3IV
    elif param == "V":
        return u.M3V
    elif param == "VI":
        return u.M3VI
    elif param == "VII":
        return u.M3VII
    elif param == "VIII":
        return u.M3VIII
    else:
        raise ValueError("Nepostojeći rotor!")


class EnigmaGUI:
    def __init__(self):
        ctk.set_appearance_mode("light")
        # customtkinter.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.bind("<Key>", self.on_key_event)
        self.root.bind("<BackSpace>", self.clear_char)
        self.root.title("Enigma Simulator")
        """
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)
        self.root.update()
        """
        self.root.state("zoomed")
        self.root.update()
        self.machine = None
        self.visualizer = EnigmaVisualizer(self.root)

        self.plaintext = ""
        self.ciphertext = ""
        self.last_path = None
        self.plugboard = None
        self.create_widgets()

    def on_key_event(self, event):
        char = event.char.upper()
        if char in u.ALPHABET:
            self.on_key_press(char)

    def reflector_choice(self, frame):
        ctk.CTkLabel(frame, text="Reflektor").grid(row=7, column=1, padx=10, pady=5)
        self.reflector_var = ctk.StringVar(value=REFLECTOR_NAMES[0])
        self.reflector_var = ctk.CTkOptionMenu(frame, values=REFLECTOR_NAMES, variable=self.reflector_var)
        self.reflector_var.grid(row=8, column=1, padx=10)

    def rotors(self, frame):
        # Rotor 1
        ctk.CTkLabel(frame, text="Levi Rotor").grid(row=0, column=0, padx=10, pady=5)
        self.left_rotor_var = ctk.StringVar(value=ROTOR_NAMES[0])
        self.left_rotor_dropdown = ctk.CTkOptionMenu(frame, values=ROTOR_NAMES, variable=self.left_rotor_var)
        self.left_rotor_dropdown.grid(row=1, column=0, padx=5)

        ctk.CTkLabel(frame, text="Pozicija").grid(row=0, column=1, padx=10)
        self.left_pos_selector = SpinnerSelector(frame, initial="A", mode="letter")
        self.left_pos_selector.grid(row=1, column=1, padx=5)

        ctk.CTkLabel(frame, text="Ringstellung").grid(row=0, column=2, padx=10)
        self.left_ring_selector = SpinnerSelector(frame, initial=0, mode="number")
        self.left_ring_selector.grid(row=1, column=2, padx=5)

        # Rotor 2
        ctk.CTkLabel(frame, text="Srednji Rotor").grid(row=2, column=0, padx=10, pady=5)
        self.middle_rotor_var = ctk.StringVar(value=ROTOR_NAMES[1])
        self.middle_rotor_dropdown = ctk.CTkOptionMenu(frame, values=ROTOR_NAMES, variable=self.middle_rotor_var)
        self.middle_rotor_dropdown.grid(row=3, column=0, padx=5)

        ctk.CTkLabel(frame, text="Pozicija").grid(row=2, column=1, padx=10)
        self.middle_pos_selector = SpinnerSelector(frame, initial="A", mode="letter")
        self.middle_pos_selector.grid(row=3, column=1, padx=5)

        ctk.CTkLabel(frame, text="Ringstellung").grid(row=2, column=2, padx=10)
        self.middle_ring_selector = SpinnerSelector(frame, initial=0, mode="number")
        self.middle_ring_selector.grid(row=3, column=2, padx=5)

        # Rotor 3
        ctk.CTkLabel(frame, text="Desni Rotor").grid(row=4, column=0, padx=10, pady=5)
        self.right_rotor_var = ctk.StringVar(value=ROTOR_NAMES[2])
        self.right_rotor_dropdown = ctk.CTkOptionMenu(frame, values=ROTOR_NAMES, variable=self.right_rotor_var)
        self.right_rotor_dropdown.grid(row=5, column=0, padx=5)

        ctk.CTkLabel(frame, text="Pozicija").grid(row=4, column=1, padx=10)
        self.right_pos_selector = SpinnerSelector(frame, initial="A", mode="letter")
        self.right_pos_selector.grid(row=5, column=1, padx=5)

        ctk.CTkLabel(frame, text="Ringstellung").grid(row=4, column=2, padx=10)
        self.right_ring_selector = SpinnerSelector(frame, initial=0, mode="number")
        self.right_ring_selector.grid(row=5, column=2, padx=5)

        for col in range(3):
            frame.grid_columnconfigure(col, weight=1)

    def outputs(self, frame):
        # Unet tekst
        self.plaintext_label = ctk.CTkLabel(frame, text="Poruka:", font=("Arial", 16))
        self.plaintext_label.pack(pady=(10, 0))

        self.plaintext_display = ctk.CTkLabel(frame, text="", font=("Courier", 18), wraplength=300)
        self.plaintext_display.pack(pady=(5, 10))
        # Šifrovan tekst
        self.ciphertext_label = ctk.CTkLabel(frame, text="Šifrovana poruka:", font=("Arial", 16))
        self.ciphertext_label.pack(pady=(10, 0))

        self.ciphertext_display = ctk.CTkLabel(frame, text="", font=("Courier", 18), wraplength=300)
        self.ciphertext_display.pack(pady=(5, 10))
        # Prostor za čuvanje prethodno šifrovanih
        self.buffer_label = ctk.CTkLabel(frame, text="Prethodno šifrovane poruke:", font=("Arial", 16))
        self.buffer_label.pack(pady=(10, 0))

        self.buffer_textbox = ctk.CTkTextbox(frame, height=150, width=300, font=("Courier", 14))
        self.buffer_textbox.pack(pady=(5, 10))
        self.buffer_textbox.configure(state="disabled")

        self.button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.button_frame.pack(pady=(0, 10))

        self.clear_button = ctk.CTkButton(self.button_frame, text="Obriši sve", command=self.clear_buffer)
        self.clear_button.pack(side="left", padx=(0, 10))  # razmak desno

        self.clear2_button = ctk.CTkButton(self.button_frame, text="Obriši", command=self.clear_char)
        self.clear2_button.pack(side="left")

        self.add_button = ctk.CTkButton(frame, text="Dodaj poruku", command=self.add_to_buffer)
        self.add_button.pack(pady=(0, 10))

    def setup_machine(self):
        left_name = self.left_rotor_var.get()
        left_position = self.left_pos_selector.get()
        left_ring = self.left_ring_selector.get()

        middle_name = self.middle_rotor_var.get()
        middle_position = self.middle_pos_selector.get()
        middle_ring = self.middle_ring_selector.get()

        right_name = self.right_rotor_var.get()
        right_position = self.right_pos_selector.get()
        right_ring = self.right_ring_selector.get()

        reflector_name = self.reflector_var.get()

        # Rotor setup
        left_rotor_w = get_wiring_for_name(left_name)
        middle_rotor_w = get_wiring_for_name(middle_name)
        right_rotor_w = get_wiring_for_name(right_name)

        left_rotor = Rotor(
            wiring=left_rotor_w[0],
            notch=left_rotor_w[1],
            position=left_position,
            ring_setting=left_ring
        )

        middle_rotor = Rotor(
            wiring=middle_rotor_w[0],
            notch=middle_rotor_w[1],
            position=middle_position,
            ring_setting=middle_ring
        )

        right_rotor = Rotor(
            wiring=right_rotor_w[0],
            notch=right_rotor_w[1],
            position=right_position,
            ring_setting=right_ring
        )

        reflector = Reflector(get_reflector_wiring(reflector_name))

        # Plugboard
        if self.plugboard is not None:
            plugboard = self.plugboard
        else:
            plugboard = Plugboard({})
        self.machine = EnigmaMachine(
            rotors=[left_rotor, middle_rotor, right_rotor],
            reflector=reflector,
            plugboard=plugboard
        )

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.param_frame = ctk.CTkFrame(main_frame)
        self.param_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.param_frame.grid_columnconfigure(0, weight=1)
        self.param_frame.grid_columnconfigure(1, weight=0)
        self.param_frame.grid_columnconfigure(2, weight=1)

        filler_lbl = ctk.CTkLabel(self.param_frame, text="", font=("Arial", 24))
        filler_lbl.grid(row=10, column=1, pady=10)
        start_button = ctk.CTkButton(self.param_frame, text="KREIRAJ MAŠINU", command=self.on_create_machine)
        start_button.grid(row=11, column=1, pady=10)

        self.visual_frame = ctk.CTkFrame(main_frame)
        self.visual_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.rotors(self.param_frame)
        self.reflector_choice(self.param_frame)

        self.output_frame = ctk.CTkFrame(main_frame)
        self.outputs(self.output_frame)
        self.output_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.rotor_display_frame = ctk.CTkFrame(main_frame)
        self.rotor_display_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        main_frame.grid_columnconfigure(0, weight=2)  # leva kolona - param ili visual
        main_frame.grid_columnconfigure(1, weight=3)  # rotor_display - malo uži centar
        main_frame.grid_columnconfigure(2, weight=4)  # output - desno

        main_frame.grid_rowconfigure(0, weight=1)
        self.visual_frame.grid_remove()

        self.bottom_frame = ctk.CTkFrame(self.root)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        separator = ctk.CTkFrame(self.bottom_frame, width=2, fg_color="gray")  # tanka vertikalna linija
        separator.grid(row=0, column=1, sticky="ns", padx=5)

        # podesimo da bottom_frame zauzme širinu
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)  # bottom_frame je "fiksna" visina

        self.plugboard_frame = ctk.CTkFrame(self.bottom_frame)
        self.plugboard_frame.grid(row=0, column=0, padx=10, sticky="ns")

        self.plugboard_widget = PlugboardWidget(self.plugboard_frame, on_update=self.on_plugboard_update)
        self.plugboard_widget.grid(row=0, column=0, columnspan=2)

        self.connection_label = ctk.CTkLabel(self.plugboard_frame, text="Konekcije:")
        self.connection_label.grid(row=1, column=0, columnspan=2)

        self.connection_list = ctk.CTkLabel(self.plugboard_frame, text="")
        self.connection_list.grid(row=2, column=0, columnspan=2)

        self.remove_last_button = ctk.CTkButton(
            self.plugboard_frame,
            text="Undo",
            command=self.on_undo_plugboard)
        self.remove_last_button.grid(row=3, column=1, sticky="s", pady=30)

        self.clear_all_button = ctk.CTkButton(
            self.plugboard_frame,
            text="Obriši sve",
            command=self.on_clear_plugboard
        )
        self.clear_all_button.grid(row=3, column=0, sticky="s", pady=30)

        self.keyboard_frame = ctk.CTkFrame(self.bottom_frame)
        self.keyboard_frame.grid(row=0, column=2, sticky="ns")

        self.keyboard = EnigmaKeyboard(self.keyboard_frame, on_key_press=self.on_key_press)
        self.keyboard.grid(row=0, column=0)

        self.output_label = ctk.CTkLabel(self.keyboard_frame, text="", font=("Arial", 14))
        self.output_label.grid(row=1, column=0, sticky="n")

        self.toggle_flow_button = ctk.CTkButton(
            self.keyboard_frame,
            text="Prikaži tok",
            command=self.toggle_visual_frame
        )
        self.toggle_flow_button.grid(row=2, column=0, pady=(5, 5))

        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.bottom_frame.grid_columnconfigure(0, weight=1)  # plugboard_frame
        self.bottom_frame.grid_columnconfigure(1, weight=0)  # separator (fiksna širina)
        self.bottom_frame.grid_columnconfigure(2, weight=1)  # keyboard_frame

    def on_create_machine(self):
        self.rotor_display_widgets = []

        self.setup_machine()

        # Očistiti prethodno
        for w in self.rotor_display_frame.winfo_children():
            w.destroy()

        for i in range(5):
            self.rotor_display_frame.grid_columnconfigure(i, weight=0)
        self.rotor_display_frame.grid_columnconfigure(0, weight=1)
        self.rotor_display_frame.grid_columnconfigure(4, weight=1)

        rotors = [self.machine.left, self.machine.middle, self.machine.right]

        for i, rotor in enumerate(rotors, start=1):
            rotor_display = RotorDisplay(
                self.rotor_display_frame,
                rotor_object=rotor,
                rotor_wiring=rotor.wiring,
                notch=rotor.notch,
                position_char=rotor.position_char()
            )
            rotor_display.grid(row=0, column=i, padx=20, pady=20)
            self.rotor_display_widgets.append(rotor_display)
            rotor_display.update_display(position_char=chr(rotor.position + u.ORD_A))

        if hasattr(self, 'lightboard'):
            self.lightboard.destroy()
        self.lightboard = LightboardKeyboard(self.rotor_display_frame)
        self.lightboard.grid(row=1, column=0, columnspan=5, pady=(10, 0))

    def on_key_press(self, letter):
        if not self.machine:
            return

        encrypted_char, path = self.machine.encrypt_letter(letter)
        self.last_path = path

        self.visualizer.visualize_letter_flow(path)
        self.output_label.configure(text=f"{letter} -> {encrypted_char}")

        self.plaintext += letter
        if encrypted_char is not None:
            self.ciphertext += encrypted_char

        self.plaintext_display.configure(text=self.plaintext)
        self.ciphertext_display.configure(text=self.ciphertext)

        self.plaintext_display.configure(text=u.safe_truncate(self.plaintext))
        self.ciphertext_display.configure(text=u.safe_truncate(self.ciphertext))

        if self.visualizer.visual_canvas:
            self.visualizer.visualize_letter_flow(path)

        rotors = [self.machine.left, self.machine.middle, self.machine.right]
        for display, rotor in zip(self.rotor_display_widgets, rotors):
            display.update_display(position_char=chr(rotor.position + u.ORD_A))

        self.lightboard.highlight_key(encrypted_char)

    def clear_char(self, event=None):
        self.plaintext = self.plaintext[:-1]
        self.ciphertext = self.ciphertext[:-1]
        self.last_path = self.last_path[:-1]
        self.plaintext_display.configure(text=self.plaintext)
        self.ciphertext_display.configure(text=self.ciphertext)

    def clear_buffer(self):
        self.plaintext = ""
        self.ciphertext = ""
        self.last_path = None
        self.plaintext_display.configure(text="")
        self.ciphertext_display.configure(text="")
        self.buffer_textbox.configure(state="normal")
        self.buffer_textbox.delete("1.0", "end")
        self.buffer_textbox.configure(state="disabled")
        self.output_label.configure(text="")

    def add_to_buffer(self):
        if not self.ciphertext:
            return

        self.buffer_textbox.configure(state="normal")
        self.buffer_textbox.insert("end", self.ciphertext + "\n" + "------------------" + "\n")
        self.buffer_textbox.configure(state="disabled")

        self.plaintext = ""
        self.ciphertext = ""
        self.last_path = None
        self.plaintext_display.configure(text="")
        self.ciphertext_display.configure(text="")
        self.output_label.configure(text="")

    def open_visual_window(self):
        if self.machine is None:
            return
        self.visualizer.open_visual_window(parent=self.visual_frame)

    def toggle_visual_frame(self):
        if self.visual_frame.winfo_ismapped():
            self.visual_frame.grid_remove()
            self.param_frame.grid()
            self.toggle_flow_button.configure(text="Prikaži tok")
        else:
            if self.machine is None:
                return
            self.param_frame.grid_remove()
            self.visual_frame.grid()
            self.open_visual_window()
            if self.last_path:
                self.visualizer.visualize_letter_flow(self.last_path)
            else:
                self.visualizer.draw_static_diagram()
            self.toggle_flow_button.configure(text="Sakrij tok")

    def on_plugboard_update(self, connections):
        try:
            # Kreiraj novi Plugboard objekat sa aktuelnim konekcijama
            self.plugboard = Plugboard(connections)

            # Update GUI labelu sa tekstom konekcija
            if connections:
                pairs_text = ", ".join(f"{a}-{b}" for a, b in connections)
            else:
                pairs_text = ""
            self.connection_list.configure(text=f"{pairs_text}")

        except ValueError as e:
            print(f"Greska u plugboard konfiguraciji: {e}")

    def on_undo_plugboard(self):
        self.plugboard_widget.remove_last_connection()

    def on_clear_plugboard(self):
        self.plugboard_widget.clear_all_connections()

    def run(self):
        self.root.mainloop()
