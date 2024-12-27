from dataclasses import dataclass
import hid
from typing import Optional

@dataclass
class ShutterM3Config:
    vendor_id: int
    product_id: int

class ShutterM3Handler:
    """Handles shutter input processing."""
    
    # Button press patterns mapped to their corresponding actions
    BUTTON_PATTERNS = {
        # Distortion (down)
        tuple([5, 60, 192, 3]): '5',
        # Overdrive (up)
        tuple([5, 60, 64, 252]): '4',
        # Preset A (left)
        tuple([5, 40, 0, 5]): 'a',
        # Preset B (right)
        tuple([5, 216, 15, 5]): 'b',
        
        # Tunner (like)
        tuple([5, 60, 128, 248]): '1',
        
        # Looper (camara)
        tuple([5, 61, 224, 252]): '2',
    }
    
    def __init__(self, config: ShutterM3Config):
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
            
    def read(self) -> Optional[str]:
        """Read and process shutter input.
        
        Returns:
            Optional[str]: The action code corresponding to the pressed button,
                          or None if no valid button press was detected.
        """
        if not self.device:
            return None
            
        try:
            data = self.device.read(64)
            if not data:
                return None
                
            # Convert the data to a tuple for dictionary lookup
            data_tuple = tuple(data[:4])  # We only need the first 4 bytes
            
            # Look up the action in our patterns dictionary
            return self.BUTTON_PATTERNS.get(data_tuple)
                
        except Exception as e:
            print(f"Error reading shutter: {e}")
            return None
            
    def cleanup(self):
        """Clean up shutter resources."""
        if self.device:
            self.device.close()
            self.device = None