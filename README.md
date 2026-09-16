# Offline AI Pet

Software-first foundation for an offline AI pet. The Mac is the AI brain; the ESP32-S3 is the physical body.

## Architecture

- **ESP32 → Mac:** validated events
- **Mac → ESP32:** validated commands
- **IDs:** every event and command has a unique ID
- **ACK:** the Mac acknowledges received events
- **Heartbeat:** supported as a protocol event
- **Offline:** no cloud service is required

## Run

From the repository root:

```bash
cd ~/pet
brain/.venv/bin/python -m pet_brain.cli demo
```

Start the Mac brain:

```bash
brain/.venv/bin/python -m pet_brain.cli server
```

In another terminal, run the virtual ESP32:

```bash
brain/.venv/bin/python -m simulator.virtual_esp32
```

Run protocol tests:

```bash
brain/.venv/bin/python -m pytest -q
```

The simulator and future ESP32 firmware will use the same event/command contract.
