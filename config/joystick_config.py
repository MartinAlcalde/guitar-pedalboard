from devices.joystick import JoystickConfig

vendor_id = 0x0810
product_id = 0x0001

actions = {
    'X': '1',          
    'SQUARE': '2',     
    'CIRCLE': '3',     
    'TRIANGLE': '4',   
    'R1': '5',         
    'R2': '6',         
    'L1': '7',         
    'L2': '8',         
    'SELECT': 'a',     
    'START': 'b',      
}

config = JoystickConfig(
    vendor_id=vendor_id,
    product_id=product_id,
    actions=actions,
    patterns={}
)