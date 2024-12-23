import time
import keyboard
from config.midi_config import midi_config
from config.joystick_config import joystick_config
from config.shutter_config import shutter_config
from devices.joystick import JoystickHandler
from devices.shutter import ShutterHandler
from midi.controller import MIDIController

def setup_keyboard_handler(midi_controller):
    """Set up keyboard event handling."""
    def key_handler(event):
        if event.event_type == keyboard.KEY_DOWN and event.name in midi_config.commands:
            midi_controller.toggle_effect(event.name)
    
    keyboard.hook(key_handler)
    return key_handler

def print_device_info(midi_controller, joystick, shutter):
    """Print information about connected devices and available commands."""
    print(f"\nMIDI Controller started on port: {midi_config.port_name}")
    print("Available commands:")
    for key, (_, effect) in midi_config.commands.items():
        print(f"Key '{key}': {effect}")
    
    if shutter and shutter.device:
        effect = midi_config.commands[shutter_config.action][1]
        print(f"\nShutter is connected and will trigger: {effect}")

    if joystick and joystick.device:
        print("\nJoystick button mappings:")
        for button, action in joystick_config.actions.items():
            effect = midi_config.commands[action][1]
            print(f"Button '{button}' will trigger: {effect}")

def main():
    # Initialize variables in wider scope
    midi_controller = None
    joystick = None
    shutter = None
    
    try:
        # Initialize controllers and devices
        midi_controller = MIDIController(midi_config)
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
            if shutter and shutter.device:
                action = shutter.read()
                if action:
                    midi_controller.toggle_effect(action)
                    
            if joystick and joystick.device:
                button = joystick.read()
                if button and button in joystick_config.actions:
                    midi_controller.toggle_effect(joystick_config.actions[button])
                    
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        keyboard.unhook_all()
        if joystick:
            joystick.cleanup()
        if shutter:
            shutter.cleanup()
        if midi_controller:
            midi_controller.cleanup()

if __name__ == "__main__":
    main()