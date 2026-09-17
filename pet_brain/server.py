import asyncio
import json

from websockets.asyncio.server import ServerConnection, serve

from pet_brain.behavior import BehaviorEngine
from pet_brain.models import PetAck, PetCommand, PetEvent
from pet_brain.protocol import new_id, now

HOST = "127.0.0.1"
PORT = 8765


class PetServer:
    def __init__(self) -> None:
        self.engine = BehaviorEngine()

    async def send_state(self, websocket: ServerConnection) -> None:
        await websocket.send(json.dumps({"type": "state", "state": self.engine.snapshot()}))

    async def send_actions(self, websocket: ServerConnection, actions: list[dict], device_id: str) -> None:
        for action in actions:
            command = PetCommand(
                command=action["command"],
                command_id=new_id("cmd"),
                device_id=device_id,
                timestamp=now(),
                expression=action.get("expression"),
                servo=action.get("servo"),
                angle=action.get("angle"),
                sound=action.get("sound"),
                value=action.get("value"),
            )
            await websocket.send(command.model_dump_json())

    async def handler(self, websocket: ServerConnection) -> None:
        await self.send_state(websocket)
        async for raw in websocket:
            try:
                event = PetEvent.model_validate_json(raw)
            except Exception as exc:
                await websocket.send(json.dumps({"type": "error", "error": "invalid_event", "detail": str(exc)}))
                continue

            detail = "heartbeat_received" if event.event == "heartbeat" else None
            await websocket.send(PetAck(message_id=event.event_id, timestamp=now(), detail=detail).model_dump_json())

            if event.event == "heartbeat":
                continue

            actions = self.engine.handle_event(event.event)
            await self.send_actions(websocket, actions, event.device_id)
            await self.send_state(websocket)


async def run_server(host: str = HOST, port: int = PORT) -> None:
    server = PetServer()
    async with serve(server.handler, host, port):
        print(f"PET BRAIN listening on ws://{host}:{port}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(run_server())
