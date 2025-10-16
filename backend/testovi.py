import utils as u
import rotor as r
import reflector as ref
import plugboard as p
import enigma_machine as em

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
M3_wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
M3_notch = "Q"


def test_rotor():
    rotor = r.Rotor(M3_wiring, M3_notch, position='A', ring_setting=0)

    print(rotor)

    # TEST ENKODIRANJA JEDNOG SLOVA
    for c in ALPHABET:
        ch = r.ltoi(c)

        enc = rotor.encode_f(ch)
        dec = rotor.encode_b(enc)
        # print(ALPHABET[enc], ALPHABET[dec])
        assert dec == ch, f"Rotor pogrešio za slovo {ch}: got {r.itol(dec)}"

    print("Test enkodiranja: Prošao!")

    print(f"Početna pozicija: {r.itol(rotor.position)}")
    for _ in range(40):
        rotor.step()
        print(f"Posle rotacije: {r.itol(rotor.position)}, rotation_needed: {rotor.rotation_needed()}")

    print("Test rotacije: Prošao!")
    print(rotor.wiring, rotor.inverse)

    for i, c in enumerate(rotor.wiring):
        inv_char = rotor.inverse[ord(c) - ord('A')]
        if inv_char != chr(i + ord('A')):
            print(f"Nije dobro na poziciji {i} ({chr(i + ord('A'))}): inverse[{c}] = {inv_char}")


test_rotor()


def test_rotation_and_encryption():
    # I, II, III, B (standard za M3)
    r1 = r.Rotor(u.EnigmaI[0], u.EnigmaI[1], position='A')
    r2 = r.Rotor(u.EnigmaII[0], u.EnigmaII[1], position='A')
    r3 = r.Rotor(u.EnigmaIII[0], u.EnigmaIII[1], position='U')  # Zbog provere double steppinga

    r_b = ref.Reflector(u.B_REFLECTOR)

    plugboard = p.Plugboard({})

    machine = em.EnigmaMachine(
        rotors=[r1, r2, r3],
        reflector=r_b,
        plugboard=plugboard
    )

    original = "OVO JE TEST ENIGMA MASINE"
    original = original.replace(" ", "")

    # encrypted = ''.join(machine.encrypt_letter(ll) for ll in original)
    encrypted = machine.encrypt_text(original)
    r1 = r.Rotor(u.EnigmaI[0], u.EnigmaI[1], position='A')
    r2 = r.Rotor(u.EnigmaII[0], u.EnigmaII[1], position='A')
    r3 = r.Rotor(u.EnigmaIII[0], u.EnigmaIII[1], position='U')  # Zbog provere double steppinga

    machine = em.EnigmaMachine(
        rotors=[r1, r2, r3],
        reflector=r_b,
        plugboard=plugboard
    )

    # decrypted = ''.join(machine.encrypt_letter(ll) for ll in encrypted)
    decrypted = machine.encrypt_text(encrypted)
    print("Original:   ", original)
    print("Encrypted:  ", encrypted)
    print("Decrypted:  ", decrypted)


test_rotation_and_encryption()


def quick_test():
    rotor_i = r.Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", position='A')
    rotor_ii = r.Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", position='A')
    rotor_iii = r.Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", position='A')

    reflector = ref.Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
    plugboard = p.Plugboard({})
    # Prva mašina
    machine1 = em.EnigmaMachine([rotor_i, rotor_ii, rotor_iii], reflector, plugboard)

    enc, _ = machine1.encrypt_letter("A")
    # Druga mašina
    rotor2_i = r.Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", position='A')
    rotor2_ii = r.Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", position='A')
    rotor2_iii = r.Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", position='A')

    machine2 = em.EnigmaMachine([rotor2_i, rotor2_ii, rotor2_iii], reflector, plugboard)

    dec, _ = machine2.encrypt_letter(enc)

    print(f"Encrypted: {enc}, Decrypted: {dec}")


quick_test()
