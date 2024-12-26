from devices.shutter import ShutterConfig

vendor_id = 0x2717
product_id = 0x0040
action = '5' # Toggle command "5" from midi_config

shutter_config = ShutterConfig(
    vendor_id=vendor_id,
    product_id=product_id,
    action=action
)