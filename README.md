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

If Ollama is unavailable, the same interface falls back to local keyword intent handling so development can continue offline.

## AI-to-WebSocket Integration

Natural-language interaction now travels through the same WebSocket path used by the virtual ESP32:

```text
User text
   ↓
AI Console
   ↓
WebSocket interaction message
   ↓
PetServer
   ↓
PetBrain
   ↓
BehaviorEngine
   ↓
WebSocket command/state
   ↓
Virtual ESP32
```

The LLM call runs outside the real-time behavior loop. Hardware commands are still produced only by the Behavior Engine and validated through `PetCommand`.

Run the server and simulators in separate terminals:

```bash
brain/.venv/bin/python -m pet_brain.server
brain/.venv/bin/python -m simulator.virtual_esp32
brain/.venv/bin/python -m simulator.ai_console
```

Then type natural language into the AI console, for example:

```text
YOU> I love you
PET: <local LLM reply> [affection]
MAC -> ESP32: {"type":"command", ...}
```

The existing `virtual_esp32` console remains useful for direct sensor-event testing.

## Run

```bash
brain/.venv/bin/python -m simulator.pet_sim
brain/.venv/bin/python -m pet_brain.server
brain/.venv/bin/python -m simulator.virtual_esp32
brain/.venv/bin/python -m pytest -q
```

The behavior loop currently runs once per second and advances one simulated minute per cycle so autonomous behavior is visible during development. This accelerated timing is temporary and will be separated from physical real-time timing during hardware integration.

## Current status

- Protocol V1.1
- Behavior Engine V1
- Autonomous Behavior Loop
- Local AI Brain V1
- Ollama structured intent integration
- Offline fallback intent handling
- Local JSON memory
- AI-to-WebSocket interaction bridge
- Virtual ESP32 end-to-end command path
- No hardware required yet
