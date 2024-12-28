import hid
from devices.shutterAB import ShutterABConfig

# IDs comunes para todos los shutters AB
vendor_id = 0x2717
product_id = 0x0040

# Encuentra todos los dispositivos AB conectados
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

# Lista de configuraciones para múltiples shutters AB
AB_SHUTTERS = find_all_ab_shutters()