# Offline AI Pet

A privacy-first desktop pet with a deterministic real-time behavior layer and a local AI brain.

## Architecture

- **Mac:** local AI brain, LLM, memory, speech, and high-level interaction.
- **ESP32-S3:** real-time body controller for sensors, display, audio, and motors.
- **WebSocket:** structured local event/command transport.
- **Behavior Engine:** deterministic state changes and hardware-safe actions.
- **Local AI Brain:** natural-language intent and short replies using Ollama, with an offline keyword fallback.
- **Memory:** local JSON storage during the development phase.

The LLM never emits hardware commands directly. It returns a small structured intent, which is translated into actions by the deterministic Behavior Engine.

## Local AI Brain

Make sure Ollama is running locally with a model available. The default model is `llama3`; override it with `PET_LLM_MODEL` if needed.

```bash
export PET_LLM_MODEL=llama3
brain/.venv/bin/python -c 'from pet_brain.brain import PetBrain; print(PetBrain().handle_text("hello"))'
```

The brain talks to Ollama at `http://127.0.0.1:11434` by default. Set `PET_OLLAMA_URL` to change it.

If Ollama is unavailable, the same interface falls back to local keyword intent handling, so the software can still be developed offline.

## Run

```bash
brain/.venv/bin/python -m simulator.pet_sim
brain/.venv/bin/python -m pet_brain.server
brain/.venv/bin/python -m simulator.virtual_esp32
brain/.venv/bin/python -m pytest -q
```

The behavior loop currently runs once per second and advances one simulated minute per cycle so autonomous behavior is visible during development. This accelerated timing is a development setting and will be separated from physical real-time timing during hardware integration.

## Current status

- Protocol V1.1
- Behavior Engine V1
- Autonomous Behavior Loop
- Local AI Brain V1
- Ollama structured intent integration
- Offline fallback intent handling
- Local JSON memory
- No hardware required yet
