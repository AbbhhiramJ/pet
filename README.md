# Offline AI Pet

Software-first foundation for a small offline AI pet.

## Architecture

- **Mac:** local AI brain, personality, memory, speech and high-level decisions.
- **ESP32-S3:** physical body, sensors, display, servos and real-time behavior.
- **Local network:** WebSocket communication between the Mac and pet.
- **Offline fallback:** the ESP32 can perform basic behavior without the Mac.

## Current milestone

The repository now includes a deterministic personality engine, validated JSON protocol models, a hardware-independent simulator, a local WebSocket Mac brain, and a virtual ESP32 client. This lets the communication loop be tested before buying hardware.

## Run

```bash
cd brain
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
python3 -m brain.cli demo
```

Start the Mac brain:

```bash
python3 -m brain.cli server
```

In another terminal run the virtual ESP32:

```bash
python3 -m simulator.virtual_esp32
```

Then send `touch`, `motion`, or `voice` events and observe the Mac responses.
