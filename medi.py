import time
import rtmidi
import keyboard

class VirtualMIDIController:
    def __init__(self):
        # Initialize MIDI output
        self.midi_out = rtmidi.MidiOut()
        self.setup_virtual_port()
        self.channel = 1  # Canal MIDI (1-16)
        self.booster_cc = 5  # CC número 5 para el Booster
        self.key = 'z'  # Tecla que activará el Booster

    def setup_virtual_port(self):
        """Crear puerto MIDI virtual"""
        # Crear un puerto virtual que aparecerá en la lista de controladores MIDI
        self.midi_out.open_virtual_port("Python MIDI Controller")
        print("\nPuerto virtual 'Python MIDI Controller' creado")
        print("Por favor, selecciona 'Python MIDI Controller' en la configuración de la Katana")

    def send_cc(self, cc_number, value):
        """Enviar mensaje MIDI Control Change"""
        status_byte = 0xB0 | (self.channel - 1)
        message = [status_byte, cc_number, value]
        self.midi_out.send_message(message)
        print(f"Enviando: Canal:{self.channel} CC#{cc_number} valor:{value}")

    def setup_keyboard_hooks(self):
        """Configurar los eventos del teclado"""
        keyboard.on_press_key(self.key, lambda _: self.send_cc(self.booster_cc, 127))
        keyboard.on_release_key(self.key, lambda _: self.send_cc(self.booster_cc, 0))

    def cleanup(self):
        """Limpiar recursos"""
        keyboard.unhook_all()
        self.midi_out.close_port()
        del self.midi_out

def main():
    try:
        # Crear y configurar el controlador
        controller = VirtualMIDIController()
        controller.setup_keyboard_hooks()
        
        print(f"\nControlador MIDI virtual iniciado!")
        print(f"Canal MIDI: {controller.channel}")
        print(f"Presiona la tecla '{controller.key}' para activar el Booster")
        print("Presiona 'Ctrl+C' para salir")
        
        # Mantener el programa corriendo
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        if 'controller' in locals():
            controller.cleanup()

if __name__ == "__main__":
    main()