from dataclasses import dataclass
import time
import hid
from typing import Dict, Optional

@dataclass
class JoystickConfig:
    vendor_id: int
    product_id: int
    actions: Dict[str, str]
    patterns: Dict[str, list]

class JoystickHandler:
    """Handles joystick input processing and button mapping."""
    
    BUTTON_MAPPING = {
        (79, 0): 'X',
        (143, 0): 'SQUARE',
        (47, 0): 'CIRCLE',
        (31, 0): 'TRIANGLE',
        (15, 8): 'R1',
        (15, 2): 'R2',
        (15, 4): 'L1',
        (15, 1): 'L2',
        (15, 16): 'SELECT',
        (15, 32): 'START'
    }
    
    IDLE_STATE = (15, 0)
    VALID_DATA_START = 1
    
    def __init__(self, config: JoystickConfig):
        self.config = config
        self.device = None
        self.last_action = None
        self.debounce_time = 0.05
        self.last_press_time = 0
        
    def connect(self):
        try:
            self.device = hid.device()
            self.device.open(self.config.vendor_id, self.config.product_id)
            self.device.set_nonblocking(True)
            return True
        except Exception as e:
            print(f"Warning: Could not connect to joystick device: {e}")
            self.device = None
            return False
            
    def process_data(self, data, current_time):
        if not data or len(data) < 8:
            return None
            
        data = list(data)
        
        if data[0] != self.VALID_DATA_START:
            return None
            
        button_state = (data[5], data[6])
        
        if button_state == self.IDLE_STATE:
            self.last_action = None
            return None
            
        button = self.BUTTON_MAPPING.get(button_state)
        if not button:
            return None
            
        if (current_time - self.last_press_time) < self.debounce_time:
            return None
            
        if button == self.last_action:
            return None
            
        self.last_action = button
        self.last_press_time = current_time
        
        return button
        
    def read(self):
        if not self.device:
            print("no joystick device found to read")
            self.connect()
            return None
            
        try:
            data = self.device.read(64)
            if not data:
                return None
                
            return self.process_data(data, time.time())
                
        except Exception as e:
            self.cleanup()
            self.connect()
            print(f"Error reading joystick: {e}")
            return None
            
    def cleanup(self):
        if self.device:
            self.device.close()
            self.device = None