from dataclasses import dataclass
import hid
from typing import Optional

@dataclass
class ShutterABConfig:
    vendor_id: int
    product_id: int


class ShutterABHandler:
    """Handles shutter input processing."""
    
    # Button press patterns mapped to their corresponding actions
    BUTTON_PATTERNS = {
        tuple([1, 1, 0]): 'a', 
        tuple([1, 2, 0]): 'b'  
    }
    
    def __init__(self, config: ShutterABConfig):
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
            print(f"Warning: Could not connect to shutter AB device: {e}")
            self.device = None
            return False
            
    def read(self) -> Optional[str]:
        """Read and process shutter input."""
        if not self.device:
            return None
            
        try:
            data = self.device.read(64)
            if not data:
                return None
                
            data_tuple = tuple(data[:3]) 
            return self.BUTTON_PATTERNS.get(data_tuple)
                
        except Exception as e:
            print(f"Error reading shutter AB: {e}")
            return None
            
    def cleanup(self):
        """Clean up shutter resources."""
        if self.device:
            self.device.close()
            self.device = None