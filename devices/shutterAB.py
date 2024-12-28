from dataclasses import dataclass
import hid
from typing import Optional

@dataclass
class ShutterABConfig:
    vendor_id: int
    product_id: int


class ShutterABHandler:
    """Handles shutter input processing."""
    
    # Class variable to track which devices are already connected
    _connected_paths = set()
    
    # Button press patterns mapped to their corresponding actions
    BUTTON_PATTERNS = {
        tuple([1, 1, 0]): 'a',
        tuple([1, 2, 0]): 'b'
    }
    
    def __init__(self, config: ShutterABConfig):
        self.config = config
        self.device = None
        self.path = None
        
    def connect(self):
        """Attempt to connect to the shutter device."""
        try:
            # Enumerate all available devices with these IDs
            devices = hid.enumerate(self.config.vendor_id, self.config.product_id)
            
            # Look for a device that isn't already connected
            for device_info in devices:
                if device_info['path'] not in self._connected_paths:
                    self.path = device_info['path']
                    self.device = hid.device()
                    self.device.open_path(self.path)
                    self.device.set_nonblocking(True)
                    self._connected_paths.add(self.path)
                    print(f"Connected to AB shutter at path: {self.path}")
                    return True
                    
            print("No available AB shutter found (all are already connected)")
            return False
            
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
            
            # Look up the action in our patterns dictionary
            action = self.BUTTON_PATTERNS.get(data_tuple)
            if action:
                print(f"AB device {self.path} action: {action}")
            return action
                
        except Exception as e:
            print(f"Error reading shutter AB: {e}")
            return None
            
    def cleanup(self):
        """Clean up shutter resources."""
        if self.device:
            if self.path in self._connected_paths:
                self._connected_paths.remove(self.path)
            self.device.close()
            self.device = None