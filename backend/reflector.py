# Komponenta kokja reflektuje signal sa jednog slova na drugo
# Reflektor ne rotira!
# Uvek se prespaja fiksnim parovima
# Reflektor enigmi daje osobinu simetricnosti!

class Reflector:
    def __init__(self, wiring: str):
        self.wiring = wiring.upper()

    def reflect(self, position: int) -> int:
        return ord(self.wiring[position]) - ord('A')