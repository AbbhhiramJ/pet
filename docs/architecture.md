# Architecture

## Principle

The robot is the body; the Mac is the brain. We validate the brain and communication protocol before buying hardware.

## Layers

```text
Sensors / actuators
        |
     ESP32-S3
        |
    WebSocket
        |
       Mac
  +-----+----------------+
  | personality          |
  | memory               |
  | local LLM            |
  | speech               |
  | vision (later)       |
  +----------------------+
```

## Responsibilities

### ESP32-S3
- Read sensors.
- Drive OLED, servos, LEDs, and audio hardware.
- Emit normalized events.
- Execute validated commands.
- Keep basic behavior alive when disconnected.

### Mac
- Maintain pet state.
- Convert events into state changes.
- Select immediate reactions.
- Call a local LLM only for language/high-level interaction.
- Handle STT/TTS and persistent memory later.

## Development rule

The simulator must reproduce the same event and command shapes that the real ESP32 firmware will use. Hardware integration should therefore replace a transport/sensor layer, not redesign the brain.
