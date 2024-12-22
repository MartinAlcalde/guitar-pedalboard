# Configuración del controlador MIDI
MIDI_CHANNEL = 1
PORT_NAME = "Python MIDI Controller"

# Mapeo de teclas a códigos MIDI (tecla: (cc_number, descripción))
COMMANDS = {
    'z': (5, 'Booster'),
    'x': (6, 'Mod'),
    'c': (7, 'Delay'),
    'v': (8, 'Reverb'),
    'b': (9, 'FX1'),
    'n': (10, 'FX2'),
}