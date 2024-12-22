# MIDI Controller Project

## Setup

To run the program:
```bash
sudo python3 medi.py
```

## Project Overview

This project aims to create a configurable MIDI controller that interacts with various programs and devices. The immediate goal is to support:
- **BIAS FX 2**
- **Boss Katana 50**

The primary goal of the project is to enable the creation of affordable pedalboards using household devices to interact with simulation software. Official footswitches for these platforms are often proprietary, expensive, and difficult to obtain.

### Compatibility
Currently, the project only supports **macOS**.

## Features

The idea is to use footswitches to control MIDI signals. These footswitches can be implemented using:
- Keyboards
- Game controllers
- USB signal emitters
- Custom-built footswitches (e.g., Bluetooth shutters)

### Vision
My original idea is to create footswitches using Bluetooth shutters, resulting in a wireless pedalboard that can:
- Toggle effects on/off
- Switch presets

## Workflow
The workflow for this project is as follows:

1. **Input:** Shutter sends a signal to the computer.
2. **Processing:** Scripts intercept the signal and map it to the corresponding MIDI code.
3. **Output:** The MIDI code is sent to the MIDI channel via the created MIDI controller.

### Example Flows
- **Turning distortion on:**
  ```
  shutter -> computer -> script intercepts signal -> maps to MIDI code -> MIDI channel -> distortion ON
  ```

- **Turning distortion off:**
  ```
  shutter -> computer -> script intercepts signal -> maps to MIDI code -> MIDI channel -> distortion OFF
  ```

## Future Goals
- Expand compatibility with additional MIDI devices and software.
- Improve the flexibility of input devices.
- Create a seamless and user-friendly experience for musicians.

---
This is a work in progress, and contributions or suggestions are welcome!
