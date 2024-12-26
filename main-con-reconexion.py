import hid
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ShutterHandler:
    def __init__(self, config):
        self.config = config
        self.device = None
        self.vendor_id = 0x2717
        self.product_id = 0x0040
        self.last_state = None

    def connect(self):
        """Conecta al dispositivo HID"""
        try:
            if self.device:
                try:
                    self.device.close()
                except:
                    pass
                self.device = None

            self.device = hid.device()
            self.device.open(self.vendor_id, self.product_id)
            self.device.set_nonblocking(1)
            
            logger.info(f"Connected to AB Shutter3")
            logger.info(f"Manufacturer: {self.device.get_manufacturer_string()}")
            logger.info(f"Product: {self.device.get_product_string()}")
            return True

        except Exception as e:
            logger.error(f"Error connecting to device: {e}")
            self.device = None
            return False

    def read(self):
        """Lee datos del dispositivo"""
        try:
            if not self.device:
                return None
            
            data = self.device.read(64)
            if data:
                # Log de los datos crudos para debug
                logger.info(f"Raw data: {[hex(x) for x in data]}")
                
                # Detecta cambios en el estado del botón
                current_state = data[0] if data else None
                if current_state != self.last_state:
                    self.last_state = current_state
                    return self.config.action
                    
            return None

        except IOError as e:
            if "read error" in str(e):
                logger.warning("Read error detected, attempting to reconnect...")
                self.connect()
            return None
        except Exception as e:
            logger.error(f"Error reading device: {e}")
            self.device = None
            return None

    def cleanup(self):
        if self.device:
            try:
                self.device.close()
            except:
                pass
        self.device = None

def main():
    try:
        shutter = ShutterHandler({
            'action': 'toggle_effect'
        })
        
        if not shutter.connect():
            logger.error("Failed to connect initially")
            return

        logger.info("Press the shutter buttons to see the raw data (Ctrl+C to exit)")
        
        while True:
            if action := shutter.read():
                logger.info(f"Action detected: {action}")
            
            if not shutter.device:
                logger.info("Device disconnected, attempting to reconnect...")
                shutter.connect()
                
            time.sleep(0.05)

    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if shutter:
            shutter.cleanup()

if __name__ == "__main__":
    main()