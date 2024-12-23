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