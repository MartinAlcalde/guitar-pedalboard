# MIDI Controller Configuration
MIDI_CHANNEL = 1
PORT_NAME = "Python MIDI Controller"

# Shutter Configuration (USB HID)
SHUTTER_VENDOR_ID = 0x248a
SHUTTER_PRODUCT_ID = 0x8266
SHUTTER_ACTION = 'z'  # The shutter will trigger the same action as this key


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