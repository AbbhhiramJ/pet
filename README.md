# Offline AI Pet

A privacy-first desktop pet with a deterministic real-time behavior layer and a local AI brain.

## Architecture

- **Mac:** local LLM, memory, speech, and high-level interaction.
- **ESP32-S3:** real-time body controller for sensors, display, audio, and motors.
- **WebSocket:** structured local event/command transport.
- **Behavior Engine:** deterministic state changes and hardware-safe actions.
- **Local AI Brain:** natural-language intent and short replies using Ollama, with an offline keyword fallback.
- **Local Speech:** microphone input is transcribed on the Mac with Whisper and then enters the same interaction pipeline.
- **Memory:** local JSON storage during development.

The LLM never emits hardware commands directly. It returns a structured intent, which is translated into actions by the deterministic Behavior Engine.

## Local AI Brain

Make sure Ollama is running locally with a model available. The default model is `llama3`; override it with `PET_LLM_MODEL`.

```bash
export PET_LLM_MODEL=llama3
brain/.venv/bin/python -c 'from pet_brain.brain import PetBrain; print(PetBrain().handle_text("hello"))'
```

The brain talks to Ollama at `http://127.0.0.1:11434` by default. Set `PET_OLLAMA_URL` to change it.

If Ollama is unavailable, the same interface falls back to local keyword intent handling.

## AI-to-WebSocket Integration

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
```

## Local Voice Input

Voice input runs entirely on the Mac. Whisper performs speech-to-text locally; the transcript is sent through the existing `PetInteraction` WebSocket path. No cloud speech API is required.

Install the updated dependencies:

```bash
cd ~/pet
brain/.venv/bin/pip install -r brain/requirements.txt
```

Run the normal server and virtual ESP32, then start the voice console:

```bash
brain/.venv/bin/python -m pet_brain.server
brain/.venv/bin/python -m simulator.virtual_esp32
brain/.venv/bin/python -m simulator.voice_console
```

Press Enter, speak for the configured recording window, and the transcript will be sent to the pet. The default recording window is 5 seconds. Change it with `--seconds` or select a smaller Whisper model during development:

```bash
brain/.venv/bin/python -m simulator.voice_console --seconds 4 --model tiny
```

The optional `--language en` flag can force a language. Without it, Whisper detects the language.

The first use of a Whisper model may download that model to the local machine. After that, transcription is local.

## Run

```bash
brain/.venv/bin/python -m simulator.pet_sim
brain/.venv/bin/python -m pet_brain.server
brain/.venv/bin/python -m simulator.virtual_esp32
brain/.venv/bin/python -m pytest -q
```

The development behavior loop currently runs once per second and advances one simulated minute per cycle so autonomous behavior is visible during testing. This accelerated timing is temporary and will be separated from physical real-time timing during hardware integration.

## Current Status

- Protocol V1.1
- Behavior Engine V1
- Autonomous Behavior Loop
- Local AI Brain V1
- Ollama structured intent integration
- Offline fallback intent handling
- Local JSON memory
- AI-to-WebSocket interaction bridge
- Local Whisper speech-to-text input
- Virtual ESP32 end-to-end command path
- No hardware required yet
