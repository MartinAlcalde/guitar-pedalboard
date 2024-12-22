# MIDI Controller Configuration
MIDI_CHANNEL = 1
PORT_NAME = "Python MIDI Controller"

# Shutter Configuration (USB HID)
SHUTTER_VENDOR_ID = 0x248a
SHUTTER_PRODUCT_ID = 0x8266
SHUTTER_ACTION = '5'  # The shutter will trigger the same action as this key

# Joystick Configuration (USB HID)
JOYSTICK_VENDOR_ID = 0x0810
JOYSTICK_PRODUCT_ID = 0x0001

# Joystick button mapping to actions
JOYSTICK_ACTIONS = {
    'X': '1',          # Will trigger same action as key '1'
    'SQUARE': '2',     # Will trigger same action as key '2'
    'CIRCLE': '3',     # Will trigger same action as key '3'
    'TRIANGLE': '4',   # Will trigger same action as key '4'
    'R1': '5',         # Will trigger same action as key '5'
    'R2': '6',         # Will trigger same action as key '6'
    'L1': '7',         # Will trigger same action as key '7'
    'L2': '8',         # Will trigger same action as key '8'
    'SELECT': 'a',     # Will trigger same action as key 'a'
    'START': 'b',      # Will trigger same action as key 'b'
}

# Joystick button patterns
JOYSTICK_PATTERNS = {
    'X': [1, 128, 128, 128, 128, 79, 0, 0],
    'SQUARE': [1, 128, 128, 128, 128, 143, 0, 0],
    'CIRCLE': [1, 128, 128, 128, 128, 47, 0, 0],
    'TRIANGLE': [1, 128, 128, 128, 128, 31, 0, 0],
    'R1': [1, 128, 128, 128, 128, 15, 8, 0],
    'R2': [1, 128, 128, 128, 128, 15, 2, 0],
    'L1': [1, 128, 128, 128, 128, 15, 4, 0],
    'L2': [1, 128, 128, 128, 128, 15, 1, 0],
    'SELECT': [1, 128, 128, 128, 128, 15, 16, 0],
    'START': [1, 128, 128, 128, 128, 15, 32, 0],
}

# Key mapping to MIDI codes (key: (cc_number, description))
# this can be used with any keyboard
COMMANDS = {
    '1': (1, 'Tunner'),
    '2': (2, 'Looper'),
    '3': (3, 'Compressor'),
    '4': (4, 'Overdrive'),
    '5': (5, 'Distortion'),
    '6': (6, 'Chorus'),
    '7': (7, 'Delay'),
    '8': (8, 'Reverb'),
    'a': (9, 'Preset A'),
    'b': (10, 'Preset B'),
    'c': (11, 'Preset C'),
    'd': (12, 'Preset D'),
    'e': (13, 'Preset E'),
    'f': (14, 'Preset F'),
    'g': (15, 'Preset G'),
    'h': (16, 'Preset H'),
}