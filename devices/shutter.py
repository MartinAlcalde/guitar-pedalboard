from dataclasses import dataclass
import hid

@dataclass
class ShutterConfig:
    vendor_id: int
    product_id: int
    action: str

class ShutterHandler:
    """Handles shutter input processing."""
    
    BUTTON_PRESS_PATTERN = [2, 2, 0]
    
    def __init__(self, config: ShutterConfig):
        self.config = config
        self.device = None
        
    def connect(self):
        """Attempt to connect to the shutter device."""
        try:
            self.device = hid.device()
            self.device.open(self.config.vendor_id, self.config.product_id)
            self.device.set_nonblocking(True)
            return True
        except Exception as e:
            print(f"Warning: Could not connect to shutter device: {e}")
            self.device = None
            return False
            
    def read(self):
        """Read and process shutter input."""
        if not self.device:
            return None
            
        try:
            data = self.device.read(64)
            if data and data == self.BUTTON_PRESS_PATTERN:
                return self.config.action
        except Exception as e:
            return None
            
    def cleanup(self):
        """Clean up shutter resources."""
        if self.device:
            self.device.close()
            self.device = None

## File: midi/controller.py
from dataclasses import dataclass
import rtmidi
import keyboard
from typing import Dict, Tuple

@dataclass
class MIDIConfig:
    channel: int
    port_name: str
    commands: Dict[str, Tuple[int, str]]

class MIDIController:
    """Handles MIDI message processing and effect state management."""
    
    def __init__(self, config: MIDIConfig):
        self.config = config
        self.midi_out = rtmidi.MidiOut()
        self.midi_out.open_virtual_port(config.port_name)
        self.states = {key: False for key in config.commands}
        
    def send_cc(self, cc_number: int, value: int):
        """Send MIDI Control Change message."""
        status_byte = 0xB0 | (self.config.channel - 1)
        self.midi_out.send_message([status_byte, cc_number, value])
        
    def toggle_effect(self, key: str):
        """Toggle effect state and send corresponding MIDI message."""
        if key not in self.config.commands:
            return
            
        cc_number, effect_name = self.config.commands[key]
        self.states[key] = not self.states[key]
        value = 127 if self.states[key] else 0
        self.send_cc(cc_number, value)
        state = "ON" if self.states[key] else "OFF"
        print(f"{effect_name}: {state}")
        
    def cleanup(self):
        """Clean up MIDI resources."""
        self.midi_out.close_port()
        del self.midi_out

## File: main.py
import time
import keyboard
from config import midi_config, joystick_config, shutter_config
from devices.joystick import JoystickHandler
from devices.shutter import ShutterHandler
from midi.controller import MIDIController, MIDIConfig

def setup_keyboard_handler(midi_controller):
    """Set up keyboard event handling."""
    def key_handler(event):
        if event.event_type == keyboard.KEY_DOWN and event.name in midi_config.COMMANDS:
            midi_controller.toggle_effect(event.name)
    
    keyboard.hook(key_handler)
    return key_handler

def print_device_info(midi_controller, joystick, shutter):
    """Print information about connected devices and available commands."""
    print(f"\nMIDI Controller started on port: {midi_config.PORT_NAME}")
    print("Available commands:")
    for key, (_, effect) in midi_config.COMMANDS.items():
        print(f"Key '{key}': {effect}")
    
    if shutter and shutter.device:
        effect = midi_config.COMMANDS[shutter_config.action][1]
        print(f"\nShutter is connected and will trigger: {effect}")

    if joystick and joystick.device:
        print("\nJoystick button mappings:")
        for button, action in joystick_config.actions.items():
            effect = midi_config.COMMANDS[action][1]
            print(f"Button '{button}' will trigger: {effect}")

def main():
    try:
        # Initialize controllers and devices
        midi_controller = MIDIController(MIDIConfig(
            midi_config.MIDI_CHANNEL,
            midi_config.PORT_NAME,
            midi_config.COMMANDS
        ))
        
        joystick = JoystickHandler(joystick_config)
        shutter = ShutterHandler(shutter_config)
        
        # Connect devices
        joystick.connect()
        shutter.connect()
        
        # Setup keyboard handling
        key_handler = setup_keyboard_handler(midi_controller)
        
        # Print device information
        print_device_info(midi_controller, joystick, shutter)
        print("\nPress 'Ctrl+C' to exit")
        
        # Main loop
        while True:
            if shutter.device:
                action = shutter.read()
                if action:
                    midi_controller.toggle_effect(action)
                    
            if joystick.device:
                button = joystick.read()
                if button and button in joystick_config.actions:
                    midi_controller.toggle_effect(joystick_config.actions[button])
                    
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        keyboard.unhook_all()
        joystick.cleanup()
        shutter.cleanup()
        midi_controller.cleanup()

if __name__ == "__main__":
    main()

## File: config/midi_config.py
# MIDI Controller Configuration
MIDI_CHANNEL = 1
PORT_NAME = "Python MIDI Controller"

# Key mapping to MIDI codes (key: (cc_number, description))
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

## File: config/joystick_config.py
from devices.joystick import JoystickConfig

VENDOR_ID = 0x0810
PRODUCT_ID = 0x0001

ACTIONS = {
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

joystick_config = JoystickConfig(
    vendor_id=VENDOR_ID,
    product_id=PRODUCT_ID,
    actions=ACTIONS,
    patterns={}  # We've removed the patterns since they're now handled in JoystickHandler
)

## File: config/shutter_config.py
from devices.shutter import ShutterConfig

VENDOR_ID = 0x248a
PRODUCT_ID = 0x8266
ACTION = '5'  # The shutter will trigger the same action as this key

shutter_config = ShutterConfig(
    vendor_id=VENDOR_ID,
    product_id=PRODUCT_ID,
    action=ACTION
)