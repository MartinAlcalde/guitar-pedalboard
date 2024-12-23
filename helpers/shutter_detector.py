import hid
import time
import rtmidi
from config.midi_config import MIDI_CHANNEL, PORT_NAME, COMMANDS

class MIDIController:
    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.midi_out.open_virtual_port(PORT_NAME)
        self.states = {key: False for key in COMMANDS}
        self.setup_hid_device()
        
    def setup_hid_device(self):
        print("\nBuscando dispositivos HID...")
        for device in hid.enumerate():
            print(f"\nID Vendedor: {device['vendor_id']:04x}")
            print(f"ID Producto: {device['product_id']:04x}")
            print(f"Fabricante: {device.get('manufacturer_string', 'N/A')}")
            print(f"Producto: {device.get('product_string', 'N/A')}")
            print(f"Path: {device['path']}")
            print("---")

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

    def cleanup(self):
        self.midi_out.close_port()
        del self.midi_out

def main():
    try:
        controller = MIDIController()
        print("\nPresiona 'Ctrl+C' para salir")
        
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nPrograma terminado")
    finally:
        if 'controller' in locals():
            controller.cleanup()

if __name__ == "__main__":
    main()