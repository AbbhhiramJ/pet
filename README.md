# Offline AI Pet

## Architecture

The pet uses a split architecture:

- **Mac** — local AI brain: LLM, STT, TTS, memory, personality and high-level reasoning.
- **ESP32-S3** — physical body: sensors, display, servos, audio and deterministic fallback behavior.
- **WebSocket** — local persistent communication between the Mac and ESP32-S3.

## Behavior Engine V1

The deterministic behavior layer sits between personality state and physical commands. It provides:

- energy, boredom and sleepiness progression
- automatic sleep/wake transitions
- mood-to-expression mapping
- bounded spontaneous idle behavior
- deterministic testing through an injectable random generator

The LLM is intentionally outside this real-time loop.
