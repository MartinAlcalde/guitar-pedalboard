import hid
import time
from typing import List, Dict

class HIDDetector:
    def __init__(self):
        self.devices: List[Dict] = []
        
    def list_devices(self) -> None:
        """List all available HID devices."""
        print("\n=== Available HID Devices ===")
        for device in hid.enumerate():
            print("\nDevice Information:")
            print(f"Vendor ID: {device['vendor_id']:04x}")
            print(f"Product ID: {device['product_id']:04x}")
            print(f"Serial Number: {device['serial_number']}")
            print(f"Manufacturer: {device['manufacturer_string']}")
            print(f"Product: {device['product_string']}")
            print(f"Interface Number: {device['interface_number']}")
            self.devices.append(device)

    def monitor_device(self, vendor_id: int, product_id: int, duration: int = 30) -> None:
        """
        Monitor a specific HID device for button presses.
        
        Args:
            vendor_id: Vendor ID in decimal format
            product_id: Product ID in decimal format
            duration: How long to monitor for button presses (in seconds)
        """
        try:
            # Open the device
            device = hid.device()
            device.open(vendor_id, product_id)
            device.set_nonblocking(True)
            
            print(f"\nMonitoring device (Vendor ID: {vendor_id:04x}, Product ID: {product_id:04x})")
            print(f"Press buttons on your device (monitoring for {duration} seconds)...")
            
            start_time = time.time()
            while time.time() - start_time < duration:
                data = device.read(64)
                if data:
                    print(f"Button Press Detected - Raw Data: {data}")
                time.sleep(0.1)
                
            device.close()
            
        except Exception as e:
            print(f"Error monitoring device: {e}")

def main():
    detector = HIDDetector()
    
    # List all available devices
    detector.list_devices()
    
    if detector.devices:
        print("\nWould you like to monitor a specific device?")
        try:
            vendor_id = int(input("Enter Vendor ID (in decimal format): "), 16)
            product_id = int(input("Enter Product ID (in decimal format): "), 16)
            duration = int(input("Enter monitoring duration in seconds (default 30): ") or "30")
            
            detector.monitor_device(vendor_id, product_id, duration)
        except ValueError as e:
            print(f"Error: Invalid input - {e}")

if __name__ == "__main__":
    main()