from backend.utils import ltoi, itol
from typing import List
from backend.rotor import Rotor
from backend.reflector import Reflector
from backend.plugboard import Plugboard


class EnigmaMachine:
    def __init__(self, rotors: List[Rotor], reflector: Reflector, plugboard: Plugboard):
        # 3 Rotora, 1 reflector, 1 plugboard

        if len(rotors) != 3:
            raise ValueError("Potrebno je tacno 3 rotora")

        self.left = rotors[0]
        self.middle = rotors[1]
        self.right = rotors[2]

        self.reflector = reflector
        self.plugboard = plugboard

    def step_rotors(self):
        # Osnovno rotiranje rotora (desni uvek)
        # pawl and ratchet sistem

        if self.middle.rotation_needed():
            self.left.step()
            # Double stepping
            self.middle.step()

        if self.right.rotation_needed():
            self.middle.step()
            print("NOTCH: " + self.right.position_char())

        self.right.step()

    def encrypt_letter(self, letter):
        # Sifrovanje jednog slova

        # Koristi se za vizuelni prikaz prolaska slova kroz mašinu
        path = [letter]

        # Ignorisanje karaktera ukoliko nije slovo
        if not letter.isalpha():
            return None, []

        # Koristimo samo velika slova
        letter = letter.upper()

        # Pokrećemo jednu iteraciju
        self.step_rotors()

        # Zamena kroz priključnu tablu
        letter = self.plugboard.swap(letter)
        path.append(letter)

        # Slovo se konvertuje u broj radi lakšeg funkcionisanja algoritma
        signal = ltoi(letter)

        # Prolazak kroz rotore unapred
        signal = self.right.encode_f(signal)
        path.append(itol(signal))
        signal = self.middle.encode_f(signal)
        path.append(itol(signal))
        signal = self.left.encode_f(signal)
        path.append(itol(signal))

        # Reflektor
        signal = self.reflector.reflect(signal)
        path.append(itol(signal))

        # Prolazak kroz rotore unazad
        signal = self.left.encode_b(signal)
        path.append(itol(signal))
        signal = self.middle.encode_b(signal)
        path.append(itol(signal))
        signal = self.right.encode_b(signal)
        path.append(itol(signal))

        # Ponovni proces kroz priključnu tablu
        letter = itol(signal)
        letter = self.plugboard.swap(letter)
        path.append(letter)

        return letter, path

    def encrypt_text(self, message: str):
        message = message.upper()
        message = message.replace(" ", "")
        result = ""
        for letter in message:
            encrypted_letter, _ = self.encrypt_letter(letter)
            if encrypted_letter:
                result += encrypted_letter
        return result
