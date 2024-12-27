from dataclasses import dataclass
import rtmidi
from typing import Dict, Tuple
from datetime import datetime


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
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] {effect_name}: {state}")
        
    def cleanup(self):
        """Clean up MIDI resources."""
        self.midi_out.close_port()
        del self.midi_out