# MIDI Controller Configuration
MIDI_CHANNEL = 1
PORT_NAME = "Python MIDI Controller"

# Key mapping to MIDI codes (key: (cc_number, description))
COMMANDS = {
    'z': (5, 'Booster'),
    'x': (6, 'Mod'),
    'c': (7, 'Delay'),
    'v': (8, 'Reverb'),
    'b': (9, 'FX1'),
    'n': (10, 'FX2'),
}