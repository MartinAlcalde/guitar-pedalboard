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