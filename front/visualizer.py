import customtkinter as ctk


class EnigmaVisualizer:
    def __init__(self, master):
        self.master = master
        self.visual_window = None
        self.visual_canvas = None

    def open_visual_window(self, parent=None):
        if parent is None:
            if self.visual_window and self.visual_window.winfo_exists():
                self.visual_window.lift()
                return

            self.visual_window = ctk.CTkToplevel(self.master)
            self.visual_window.title("Tok signala kroz Enigmu")
            self.visual_window.geometry("500x500")

            if self.visual_canvas is not None:
                self.visual_canvas.destroy()

            self.visual_canvas = ctk.CTkCanvas(
                self.visual_window,
                width=500,
                height=500,
                bg="#1e1e1e",
                highlightthickness=0
            )
            self.visual_canvas.pack(padx=10, pady=10, fill="both", expand=True)

        else:
            # Ako je parent prosleđen, crtamo unutar parent frame-a
            if self.visual_canvas is not None:
                self.visual_canvas.destroy()

            # Ako je otvoren Toplevel prozor, zatvori ga da nema duplih prikaza
            if self.visual_window and self.visual_window.winfo_exists():
                self.visual_window.destroy()
                self.visual_window = None

            self.visual_canvas = ctk.CTkCanvas(
                parent,
                width=500,
                height=500,
                bg="#1e1e1e",
                highlightthickness=0
            )
            self.visual_canvas.pack(padx=10, pady=10, fill="both", expand=True)

        self.draw_static_diagram()

    def draw_static_diagram(self):
        if not self.visual_canvas or not self.visual_canvas.winfo_exists():
            return

        canvas = self.visual_canvas
        canvas.delete("all")

        blocks = [
            ("Plugboard", 10),
            ("Rotor R", 70),
            ("Rotor M", 130),
            ("Rotor L", 190),
            ("Reflector", 250),
            ("Rotor L", 310),
            ("Rotor M", 370),
            ("Rotor R", 430),
            ("Plugboard", 490)
        ]

        for label, y in blocks:
            canvas.create_rectangle(160, y, 240, y + 40,
                                    fill="gray" if label == "Plugboard" else "darkblue", outline="white")
            canvas.create_text(200, y + 20, text=label, fill="white")

        canvas.create_rectangle(160, 250, 240, 290, fill="goldenrod", outline="white")
        canvas.create_text(200, 270, text="Reflector", fill="black")

        arrow_y = [50, 110, 170, 230, 290, 350, 410, 470]
        for y in arrow_y:
            canvas.create_line(200, y, 200, y+20, arrow="last", fill="white")

    def visualize_letter_flow(self, path):
        if not self.visual_canvas or not path or len(path) < 2 or not self.visual_canvas.winfo_exists():
            return

        self.draw_static_diagram()
        canvas = self.visual_canvas

        # Parovi ulaz izlaz
        pairs = list(zip(path[:-1], path[1:]))

        y_positions = [
            30, 90, 150, 210, 270, 330, 390, 450, 510
        ]

        x_from = 300
        x_to = 400

        stage_labels = [
            "Plugboard",
            "Rotor R",
            "Rotor M",
            "Rotor L",
            "Reflector",
            "Rotor L unazad",
            "Rotor M unazad",
            "Rotor R unazad",
            "Plugboard unazad"
        ]

        for i, (inp, outp) in enumerate(pairs):
            if i >= len(y_positions):
                break

            y = y_positions[i]

            canvas.create_line(x_from + 40, y, x_to, y, arrow="last", fill="cyan", width=2)

            # Prikaz ulaznog i izlaznog slova
            canvas.create_text(x_from + 20, y, text=inp, fill="white", font=("Courier", 14, "bold"))
            canvas.create_text(x_to + 10, y, text=outp, fill="cyan", font=("Courier", 14, "bold"))

            canvas.create_text(20, y, text=stage_labels[i], anchor="w", fill="gray", font=("Arial", 10, "italic"))

