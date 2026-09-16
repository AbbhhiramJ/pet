# Offline AI Pet

Software-first foundation for an offline AI pet. The Mac is the AI brain; the ESP32-S3 is the physical body.

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

The simulator and real firmware will use the same event/command protocol.
