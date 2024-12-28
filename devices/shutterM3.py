from dataclasses import dataclass
import hid
from typing import Optional

@dataclass
class ShutterM3Config:
    vendor_id: int
    product_id: int


class ShutterM3Handler:
    """Handles shutter input processing."""
    
    # Class variable to track which devices are already connected
    _connected_paths = set()
    
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
        # Looper (camera)
        tuple([5, 61, 224, 252]): '2',
    }
    
    def __init__(self, config: ShutterM3Config):
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
                    print(f"Connected to M3 shutter at path: {self.path}")
                    return True
                    
            print("No available M3 shutter found (all are already connected)")
            return False
            
        except Exception as e:
            print(f"Warning: Could not connect to shutter M3 device: {e}")
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
                
            data_tuple = tuple(data[:4])  # We need the first 4 bytes for M3
            
            # Look up the action in our patterns dictionary
            action = self.BUTTON_PATTERNS.get(data_tuple)
            if action:
                print(f"M3 device {self.path} action: {action}")
            return action
                
        except Exception as e:
            print(f"Error reading shutter M3: {e}")
            return None
            
    def cleanup(self):
        """Clean up shutter resources."""
        if self.device:
            if self.path in self._connected_paths:
                self._connected_paths.remove(self.path)
            self.device.close()
            self.device = None