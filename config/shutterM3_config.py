import hid
from devices.shutterM3 import ShutterM3Config

# Common IDs for all M3 shutters
vendor_id = 0x05ac
product_id = 0x022c

# Find all connected M3 devices
def find_all_m3_shutters():
    devices = hid.enumerate(vendor_id, product_id)
    configs = []
    
    for device in devices:
        configs.append(ShutterM3Config(
            vendor_id=vendor_id,
            product_id=product_id
        ))
    
    print(f"Found {len(configs)} M3 shutter(s)")
    return configs

# List of configurations for multiple M3 shutters
M3_SHUTTERS = find_all_m3_shutters()