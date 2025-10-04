# Mehanički disk sa unutrašnjim prespajanjem od 26 slova
# Ulazno slovo mapira na drugo slovo
# Niz od 26 karaktera, postoji zarez koji gura sledeći rotor
# Trenutna rotacija
# Ringstellung - početno pomeranje rotora (dodatna sigurnost)
# Postoji forward i reverse pravac

# Ove dve funkcije postoje kako bi se verodostojnije prikazao rad enigma masine
# Pozicija na masini je bila slovo, ali mi koristimo broj radi lakseg rada

from utils import ORD_A, ALPHABET_NUM, ltoi, itol


class Rotor:
    def __init__(self, wiring: str, notch: str, position: str = 'A', ring_setting: int = 0):
        self.wiring = wiring
        self.notch = notch
        self.position = ltoi(position)
        self.ring_setting = ring_setting % ALPHABET_NUM

        self.inverse = [''] * ALPHABET_NUM
        for i, c in enumerate(wiring):
            self.inverse[ord(c) - ORD_A] = chr(i + ORD_A)
        self.inverse = ''.join(self.inverse)

    def step(self):
        # Rotacija rotora
        self.position = (self.position + 1) % ALPHABET_NUM

    def rotation_needed(self):
        # Da li treba da se aktivira sledeci rotor
        curr = itol(self.position)
        return curr == self.notch

    def encode_f(self, c):
        shift = (c + self.position - self.ring_setting) % ALPHABET_NUM
        enc_char = self.wiring[shift]
        result = (ord(enc_char) - ORD_A - self.position + self.ring_setting) % ALPHABET_NUM
        return result

    def encode_b(self, c):
        shift = (c + self.position - self.ring_setting) % ALPHABET_NUM
        enc_char = self.inverse[shift]
        result = (ord(enc_char) - ORD_A - self.position + self.ring_setting) % ALPHABET_NUM
        return result
