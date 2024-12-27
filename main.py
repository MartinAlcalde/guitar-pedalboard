import time
from config.midi_config import midi_config
from config.joystick_config import joystick_config
from config.shutter_config import shutter_config
from devices.joystick import JoystickHandler
from devices.shutter import ShutterHandler
from midi.controller import MIDIController

def print_device_info(midi_controller, joystick, shutter):
    """Print information about connected devices and available commands."""
    print(f"\nMIDI Controller started on port: {midi_config.port_name}")
    
    if shutter and shutter.device:
        print("\nShutter connected with mappings:")
        for pattern, action in shutter.BUTTON_PATTERNS.items():
            effect = midi_config.commands[action][1]
            print(f"Button pattern {pattern} -> {effect}")

    if joystick and joystick.device:
        print("\nJoystick connected with mappings:")
        for button, action in joystick_config.actions.items():
            effect = midi_config.commands[action][1]
            print(f"Button '{button}' -> {effect}")

def main():
    try:
        # Initialize and connect devices
        midi_controller = MIDIController(midi_config)
        
        joystick = JoystickHandler(joystick_config)
        joystick.connect()
        
        shutter = ShutterHandler(shutter_config)
        shutter.connect()
        
        # Print device information
        print_device_info(midi_controller, joystick, shutter)
        print("\nPress 'Ctrl+C' to exit")
        
        # Main loop
        while True:
            # Check shutter input
            if shutter.device:
                if action := shutter.read():
                    midi_controller.toggle_effect(action)
                    
            # Check joystick input
            if joystick.device:
                if button := joystick.read():
                    if action := joystick_config.actions.get(button):
                        midi_controller.toggle_effect(action)
                    
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        if joystick:
            joystick.cleanup()
        if shutter:
            shutter.cleanup()
        if midi_controller:
            midi_controller.cleanup()

if __name__ == "__main__":
    main()