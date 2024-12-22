import rtmidi

def list_all_midi_ports():
    """Lista todos los puertos MIDI del sistema"""
    
    # Listar puertos de entrada
    midi_in = rtmidi.MidiIn()
    print("\nPuertos MIDI de entrada disponibles:")
    ports = midi_in.get_ports()
    for i, port in enumerate(ports):
        print(f"{i}: {port}")
    
    # Listar puertos de salida
    midi_out = rtmidi.MidiOut()
    print("\nPuertos MIDI de salida disponibles:")
    ports = midi_out.get_ports()
    for i, port in enumerate(ports):
        print(f"{i}: {port}")

    # Cleanup
    del midi_in
    del midi_out

if __name__ == "__main__":
    list_all_midi_ports()