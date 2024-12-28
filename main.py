import time
from config.midi_config import midi_config
from config.joystick_config import joystick_config
from config.shutterM3_config import M3shutter_config
from config.shutterAB_config import AB_SHUTTERS
from devices.joystick import JoystickHandler
from devices.shutterM3 import ShutterM3Handler
from devices.shutterAB import ShutterABHandler
from midi.controller import MIDIController

class DeviceManager:
    def __init__(self):
        self.handlers = []
        self.midi_controller = None

    def add_handler(self, handler):
        if handler.connect():
            self.handlers.append(handler)
            return True
        return False
            
    def print_device_info(self):
        print(f"\nMIDI Controller started on port: {midi_config.port_name}")
        
        # Agrupar handlers por tipo
        handler_groups = {}
        for handler in self.handlers:
            handler_type = handler.__class__.__name__
            if handler_type not in handler_groups:
                handler_groups[handler_type] = []
            handler_groups[handler_type].append(handler)
            
        # Imprimir información por grupo
        for handler_type, handlers in handler_groups.items():
            if handlers:
                print(f"\n{handler_type}: {len(handlers)} device(s) connected")
                for i, handler in enumerate(handlers, 1):
                    if isinstance(handler, (ShutterM3Handler, ShutterABHandler)):
                        print(f"\n{handler_type} #{i} mappings:")
                        for pattern, action in handler.BUTTON_PATTERNS.items():
                            effect = midi_config.commands[action][1]
                            print(f"Button pattern {pattern} -> {effect}")
                    elif isinstance(handler, JoystickHandler):
                        print(f"\nJoystick #{i} mappings:")
                        for button, action in joystick_config.actions.items():
                            effect = midi_config.commands[action][1]
                            print(f"Button '{button}' -> {effect}")

    def process_inputs(self):
        for handler in self.handlers:
            if isinstance(handler, ShutterM3Handler) or isinstance(handler, ShutterABHandler):
                if action := handler.read():
                    self.midi_controller.toggle_effect(action)
            elif isinstance(handler, JoystickHandler):
                if button := handler.read():
                    if action := joystick_config.actions.get(button):
                        self.midi_controller.toggle_effect(action)

    def cleanup(self):
        for handler in self.handlers:
            handler.cleanup()
        if self.midi_controller:
            self.midi_controller.cleanup()

def main():
    try:
        device_manager = DeviceManager()
        device_manager.midi_controller = MIDIController(midi_config)
        
        # Initialize handlers
        device_manager.add_handler(JoystickHandler(joystick_config))
        device_manager.add_handler(ShutterM3Handler(M3shutter_config))
        
        # Inicializar todos los shutters AB encontrados
        ab_connected = 0
        for shutter_config in AB_SHUTTERS:
            if device_manager.add_handler(ShutterABHandler(shutter_config)):
                ab_connected += 1
                
        print(f"Connected to {ab_connected} AB shutter(s)")
        
        # Print device information
        device_manager.print_device_info()
        print("\nPress 'Ctrl+C' to exit")
        
        # Main loop
        while True:
            device_manager.process_inputs()
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        device_manager.cleanup()

if __name__ == "__main__":
    main()