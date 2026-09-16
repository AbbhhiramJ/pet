import asyncio
import json

from websockets.asyncio.server import ServerConnection, serve

from pet_brain.models import PetAck, PetCommand, PetEvent
from pet_brain.personality import PersonalityEngine
from pet_brain.protocol import new_id, now

HOST = "127.0.0.1"
PORT = 8765

class PetServer:
    def __init__(self) -> None:
        self.engine = PersonalityEngine()

    async def send_state(self, websocket: ServerConnection) -> None:
        await websocket.send(json.dumps({"type": "state", "state": self.engine.snapshot()}))

    async def handler(self, websocket: ServerConnection) -> None:
        await self.send_state(websocket)
        async for raw in websocket:
            try:
                event = PetEvent.model_validate_json(raw)
            except Exception as exc:
                await websocket.send(json.dumps({"type": "error", "error": "invalid_event", "detail": str(exc)}))
                continue

            ack = PetAck(message_id=event.event_id, timestamp=now())
            await websocket.send(ack.model_dump_json())

            if event.event == "heartbeat":
                await websocket.send(PetAck(message_id=event.event_id, timestamp=now(), detail="heartbeat_received").model_dump_json())
                continue

            for action in self.engine.handle(event.event):
                command = PetCommand(
                    command=action["command"],
                    command_id=new_id("cmd"),
                    device_id=event.device_id,
                    timestamp=now(),
                    expression=action.get("expression"),
                    servo=action.get("servo"),
                    angle=action.get("angle"),
                    sound=action.get("sound"),
                    value=action.get("value"),
                )
                await websocket.send(command.model_dump_json())

            await self.send_state(websocket)

async def run_server(host: str = HOST, port: int = PORT) -> None:
    server = PetServer()
    async with serve(server.handler, host, port):
        print(f"PET BRAIN listening on ws://{host}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(run_server())
