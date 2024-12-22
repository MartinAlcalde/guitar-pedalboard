import time
import rtmidi
import keyboard
import hid
from midi_config import (
    MIDI_CHANNEL, 
    PORT_NAME, 
    COMMANDS, 
    SHUTTER_VENDOR_ID, 
    SHUTTER_PRODUCT_ID, 
    SHUTTER_ACTION
)

class MIDIController:
    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.midi_out.open_virtual_port(PORT_NAME)
        self.states = {key: False for key in COMMANDS}
        self.setup_keyboard_hooks()
        self.setup_shutter()
        
    def setup_shutter(self):
        try:
            self.shutter = hid.device()
            self.shutter.open(SHUTTER_VENDOR_ID, SHUTTER_PRODUCT_ID)
            self.shutter.set_nonblocking(True)
            print(f"\nShutter connected")
        except Exception as e:
            print(f"Warning: Could not connect to shutter device: {e}")
            self.shutter = None

    def read_shutter(self):
        if not hasattr(self, 'shutter') or self.shutter is None:
            return
            
        try:
            data = self.shutter.read(64)
            if data and data == [2, 2, 0]:  # Shutter button press
                self.toggle_effect(SHUTTER_ACTION)
        except Exception as e:
            pass  # Ignore read errors

    def send_cc(self, cc_number, value):
        status_byte = 0xB0 | (MIDI_CHANNEL - 1)
        self.midi_out.send_message([status_byte, cc_number, value])

    def toggle_effect(self, key):
        if key not in COMMANDS:
            return
            
        cc_number, effect_name = COMMANDS[key]
        self.states[key] = not self.states[key]
        value = 127 if self.states[key] else 0
        self.send_cc(cc_number, value)
        state = "ON" if self.states[key] else "OFF"
        print(f"{effect_name}: {state}")

    def key_handler(self, event):
        if event.event_type == keyboard.KEY_DOWN and event.name in COMMANDS:
            self.toggle_effect(event.name)

    def setup_keyboard_hooks(self):
        keyboard.hook(self.key_handler)

    def cleanup(self):
        keyboard.unhook_all()
        if hasattr(self, 'shutter') and self.shutter is not None:
            self.shutter.close()
        self.midi_out.close_port()
        del self.midi_out

def main():
    try:
        controller = MIDIController()
        print(f"\nMIDI Controller started on port: {PORT_NAME}")
        print("Available commands:")
        for key, (_, effect) in COMMANDS.items():
            print(f"Key '{key}': {effect}")
        print("\nPress 'Ctrl+C' to exit")
        
        while True:
            controller.read_shutter()
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        if 'controller' in locals():
            controller.cleanup()

if __name__ == "__main__":
    main()