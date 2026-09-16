# Pet Protocol

Transport: WebSocket over the local network.

## Event

ESP32 → Mac:

```json
{"type":"event","event":"touch","timestamp":1789549000,"value":1}
```

Events describe something that happened. They are validated before entering the personality engine.

## Command

Mac → ESP32:

```json
{"type":"command","command":"set_expression","expression":"happy"}
```

Commands describe an action for the physical pet.

## State

Mac → ESP32 after an event:

```json
{"type":"state","state":{"mood":"happy","energy":79.5}}
```

## Error

Invalid messages receive an error object rather than entering the behavior loop.

## Connection behavior

1. ESP32 connects to the Mac server.
2. Mac sends current state.
3. ESP32 sends events.
4. Mac validates events and updates personality.
5. Mac sends commands and updated state.
6. If the connection drops, ESP32 enters basic local behavior and retries.

The protocol is intentionally small for V1.
