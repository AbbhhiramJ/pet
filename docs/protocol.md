# Pet Protocol

Transport: WebSocket over the local network.

## Event

ESP32 → Mac:

```json
{"type":"event","event":"touch","timestamp":1789549000,"value":1}
```

Events describe something that happened. They should be small, serializable, and independent of hardware-specific implementation details.

## Command

Mac → ESP32:

```json
{"type":"command","command":"set_expression","expression":"happy"}
```

Commands describe an action for the physical pet.

## Connection behavior

1. ESP32 connects to the Mac server.
2. ESP32 sends a heartbeat.
3. Events are queued and transmitted without blocking sensor handling.
4. Mac sends commands.
5. If the connection drops, ESP32 enters basic local behavior and retries.

The protocol is intentionally small for V1. New fields should be added only when a real requirement appears.
