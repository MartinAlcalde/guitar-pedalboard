from midi.controller import MIDIConfig

# MIDI Configuration
midi_channel = 1
port_name = "Python MIDI Controller"

# Key mapping to MIDI codes (key: (cc_number, description))
commands = {
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

midi_config = MIDIConfig(
    channel=midi_channel,
    port_name=port_name,
    commands=commands
)