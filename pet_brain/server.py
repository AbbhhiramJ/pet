import asyncio
import json

from websockets.asyncio.server import ServerConnection, serve

from pet_brain.models import PetEvent
from pet_brain.personality import PersonalityEngine

HOST = "127.0.0.1"
PORT = 8765

class PetServer:
    def __init__(self) -> None:
        self.engine = PersonalityEngine()

    async def handler(self, websocket: ServerConnection) -> None:
        await websocket.send(json.dumps({"type":"state", "state":self.engine.snapshot()}))
        async for raw in websocket:
            try:
                event = PetEvent.model_validate_json(raw)
            except Exception as exc:
                await websocket.send(json.dumps({"type":"error", "error":"invalid_event", "detail":str(exc)}))
                continue
            for command in self.engine.handle(event.event):
                await websocket.send(json.dumps({"type":"command", **command}))
            await websocket.send(json.dumps({"type":"state", "state":self.engine.snapshot()}))

async def run_server(host: str = HOST, port: int = PORT) -> None:
    server = PetServer()
    async with serve(server.handler, host, port):
        print(f"PET BRAIN listening on ws://{host}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(run_server())
