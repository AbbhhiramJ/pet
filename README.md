# Offline AI Pet

A software-first foundation for a small offline AI pet.

## Architecture

- **Mac:** AI brain — local LLM, speech, memory, personality, and high-level decisions.
- **ESP32-S3:** physical body — sensors, display, servos, audio, and real-time behavior.
- **Local network:** WebSocket connection between the Mac and pet.
- **Offline fallback:** the ESP32 can perform basic behavior without the Mac.

## Current milestone

This repository starts with a hardware-independent simulator and protocol. The simulator lets us validate the complete event → personality → command loop before purchasing hardware.

## Run

```bash
cd brain
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m brain.cli demo
```

The simulator can also be run directly:

```bash
python -m simulator.pet_sim
```

See `docs/architecture.md` and `docs/protocol.md` for the design.
