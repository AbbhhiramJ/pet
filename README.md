# Offline AI Pet

A privacy-first desktop pet with a deterministic real-time behavior layer and a future local AI brain.

## Architecture

- **Mac:** local AI brain, LLM, speech, memory, and high-level interaction.
- **ESP32-S3:** real-time body controller for sensors, display, audio, and motors.
- **WebSocket:** structured local event/command transport.
- **Behavior Engine:** deterministic sensor reactions, mood/expression mapping, idle behavior, and sleep/wake state.

The LLM is intentionally outside the real-time sensor loop.

## Run

```bash
brain/.venv/bin/python -m simulator.pet_sim
brain/.venv/bin/python -m pet_brain.server
brain/.venv/bin/python -m simulator.virtual_esp32
brain/.venv/bin/python -m pytest -q
```

## Current status

- Protocol V1.1: event IDs, command IDs, device identity, timestamps, ACKs, heartbeat, and strict validation.
- Behavior Engine V1: deterministic interactions, boredom/energy/sleepiness progression, sleep/wake, idle behavior, and expression mapping.
- WebSocket server: routes supported ESP32 events through the Behavior Engine and returns structured commands/state.
