import time
import rtmidi
import keyboard

class VirtualMIDIController:
    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.setup_virtual_port()
        self.channel = 1
        self.booster_cc = 5
        self.key = 'z'
        self.is_on = False
        self.press_count = 0  # Contador de pulsaciones para depuración

    def setup_virtual_port(self):
        self.midi_out.open_virtual_port("Python MIDI Controller")
        print("\nPuerto virtual 'Python MIDI Controller' creado")
        print("Por favor, selecciona 'Python MIDI Controller' en la configuración de la Katana")

    def send_cc(self, cc_number, value):
        status_byte = 0xB0 | (self.channel - 1)
        message = [status_byte, cc_number, value]
        self.midi_out.send_message(message)
        print(f"Enviando: Canal:{self.channel} CC#{cc_number} valor:{value}")

    def toggle_booster(self, event):
        """Toggle del estado del booster con información de depuración"""
        self.press_count += 1
        self.is_on = not self.is_on
        value = 127 if self.is_on else 0
        print(f"\nPulsación #{self.press_count}")
        print(f"Evento de tecla: {event}")
        print(f"Estado anterior: {'ON' if not self.is_on else 'OFF'}")
        print(f"Nuevo estado: {'ON' if self.is_on else 'OFF'}")
        self.send_cc(self.booster_cc, value)

    def setup_keyboard_hooks(self):
        """Configurar los eventos del teclado usando un enfoque diferente"""
        keyboard.hook(self.key_handler)  # Usamos hook en lugar de on_press_key

    def key_handler(self, event):
        """Manejador de eventos de teclado más detallado"""
        if event.name == self.key and event.event_type == keyboard.KEY_DOWN:
            self.toggle_booster(event)

    def cleanup(self):
        keyboard.unhook_all()
        self.midi_out.close_port()
        del self.midi_out

def main():
    try:
        controller = VirtualMIDIController()
        controller.setup_keyboard_hooks()
        
        print(f"\nControlador MIDI virtual iniciado!")
        print(f"Canal MIDI: {controller.channel}")
        print(f"Presiona la tecla '{controller.key}' para activar/desactivar el Booster")
        print("Presiona 'Ctrl+C' para salir")
        
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