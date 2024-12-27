from devices.shutterM3 import ShutterM3Config

# este es el shutter que tengo en el pedal
vendor_id = 0x05ac
product_id = 0x022c

shutter_config = ShutterM3Config(
    vendor_id=vendor_id,
    product_id=product_id
)