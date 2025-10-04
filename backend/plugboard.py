# Steckerbrett (nemacki)
# Dodatno menja slova pre nego sto udju u rotore

class Plugboard:
    def __init__(self, wiring=None):
        self.mapping = {}

        if wiring:
            for first, second in wiring:
                first = first.upper()
                second = second.upper()

                if first == second:
                    raise ValueError(f"Karakter {first} ne sme da se spaja sam sa sobom.")
                if first in self.mapping or second in self.mapping:
                    raise ValueError(f"Slovo {first} ili {second} je vec povezano.")

                self.mapping[first] = second
                self.mapping[second] = first

    def swap(self, first):
        # Vrati slovo (zavisi od mapiranja)
        return self.mapping.get(first.upper(), first.upper())


# Primer koriscenja

"""
plugboard = Plugboard([('A', 'M'), ('G', 'L'), ('T', 'P')])

print(plugboard.swap('A'))  # → 'M'
print(plugboard.swap('M'))  # → 'A'
print(plugboard.swap('T'))  # → 'P'
print(plugboard.swap('X'))  # → 'X' (nije povezano)
"""
