import hid
import time
from collections import OrderedDict

def test_joystick():
    VENDOR_ID = 0x0810
    PRODUCT_ID = 0x0001
    
    try:
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        device.set_nonblocking(True)
        
        print("\nTwin USB Joystick connected")
        print("Move the joystick, press buttons, etc.")
        print("Press Ctrl+C to exit\n")
        
        # Usar OrderedDict para mantener el orden de detección
        unique_patterns = OrderedDict()
        
        while True:
            try:
                data = device.read(64)
                if data:
                    # Convertir a tuple para poder usarlo como key en el dict
                    data_tuple = tuple(data)
                    if data_tuple not in unique_patterns:
                        print(f"New pattern detected: {list(data)}")
                        unique_patterns[data_tuple] = True
                    
            except KeyboardInterrupt:
                break
            except:
                pass
            
            time.sleep(0.01)
            
        # Mostrar resumen
        print("\n=== Summary of unique patterns detected ===")
        for i, pattern in enumerate(unique_patterns.keys(), 1):
            print(f"\nPattern {i}:")
            print(f"Data: {list(pattern)}")
            
    except Exception as e:
        print(f"Error connecting to joystick: {e}")
    finally:
        if 'device' in locals():
            device.close()

if __name__ == "__main__":
    test_joystick()