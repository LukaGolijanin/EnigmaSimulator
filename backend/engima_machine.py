from utils import ltoi, itol
from typing import List
from rotor import Rotor
from reflector import Reflector
from plugboard import Plugboard


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

        self.right.step()

        if self.right.rotation_needed():
            self.middle.step()

        if self.middle.rotation_needed():
            self.left.step()
            # Double steppingc
            self.middle.step()

    def encrypt_letter(self, letter):
        # Sifrovanje jednog slova

        if not letter.isalpha():
            return letter  # ignorisanje

        letter = letter.upper()

        self.step_rotors()

        letter = self.plugboard.swap(letter)

        signal = ltoi(letter)

        # Rotor unapred
        signal = self.right.encode_f(signal)
        signal = self.middle.encode_f(signal)
        signal = self.left.encode_f(signal)

        # Reflector
        signal = self.reflector.reflect(signal)

        # Rotor unazad
        signal = self.left.encode_b(signal)
        signal = self.middle.encode_b(signal)
        signal = self.right.encode_b(signal)

        # Ponovo plugboard
        letter = itol(signal)
        letter = self.plugboard.swap(letter)

        return letter
