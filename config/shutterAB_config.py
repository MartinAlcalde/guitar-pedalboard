import hid
from devices.shutterAB import ShutterABConfig

# Common IDs for all AB shutters
vendor_id = 0x2717
product_id = 0x0040

# Find all connected AB devices
def find_all_ab_shutters():
    devices = hid.enumerate(vendor_id, product_id)
    configs = []
    
    for device in devices:
        configs.append(ShutterABConfig(
            vendor_id=vendor_id,
            product_id=product_id
        ))
    
    print(f"Found {len(configs)} AB shutter(s)")
    return configs

# List of configurations for multiple AB shutters
AB_SHUTTERS = find_all_ab_shutters()