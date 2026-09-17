import asyncio
import json

from websockets.asyncio.server import ServerConnection, serve

from pet_brain.behavior import BehaviorEngine
from pet_brain.models import PetAck, PetCommand, PetEvent
from pet_brain.protocol import new_id, now

HOST = "127.0.0.1"
PORT = 8765
BEHAVIOR_INTERVAL_SECONDS = 1.0
SIMULATED_MINUTES_PER_CYCLE = 1.0


class PetServer:
    def __init__(self) -> None:
        self.engine = BehaviorEngine()
        self.clients: set[ServerConnection] = set()

    async def send_state(self, websocket: ServerConnection) -> None:
        await websocket.send(json.dumps({"type": "state", "state": self.engine.snapshot()}))

    async def send_actions(self, websocket: ServerConnection, actions: list[dict], device_id: str) -> None:
        for action in actions:
            command = PetCommand(
                command=action["command"], command_id=new_id("cmd"), device_id=device_id, timestamp=now(),
                expression=action.get("expression"), servo=action.get("servo"), angle=action.get("angle"),
                sound=action.get("sound"), value=action.get("value"),
            )
            await websocket.send(command.model_dump_json())

    async def broadcast_actions(self, actions: list[dict]) -> None:
        if not actions or not self.clients:
            return
        dead_clients: set[ServerConnection] = set()
        for websocket in tuple(self.clients):
            try:
                await self.send_actions(websocket, actions, "virtual-esp32")
                await self.send_state(websocket)
            except Exception:
                dead_clients.add(websocket)
        self.clients.difference_update(dead_clients)

    async def behavior_loop(self) -> None:
        while True:
            await asyncio.sleep(BEHAVIOR_INTERVAL_SECONDS)
            actions = self.engine.tick(SIMULATED_MINUTES_PER_CYCLE)
            actions.extend(self.engine.idle())
            await self.broadcast_actions(actions)

    async def handler(self, websocket: ServerConnection) -> None:
        self.clients.add(websocket)
        try:
            await self.send_state(websocket)
            async for raw in websocket:
                try:
                    event = PetEvent.model_validate_json(raw)
                except Exception as exc:
                    await websocket.send(json.dumps({"type": "error", "error": "invalid_event", "detail": str(exc)}))
                    continue
                detail = "heartbeat_received" if event.event == "heartbeat" else None
                ack = PetAck(message_id=event.event_id, timestamp=now(), detail=detail)
                await websocket.send(ack.model_dump_json())
                if event.event == "heartbeat":
                    continue
                actions = self.engine.handle_event(event.event)
                await self.send_actions(websocket, actions, event.device_id)
                await self.send_state(websocket)
        finally:
            self.clients.discard(websocket)


async def run_server(host: str = HOST, port: int = PORT) -> None:
    server = PetServer()
    behavior_task = asyncio.create_task(server.behavior_loop())
    try:
        async with serve(server.handler, host, port):
            print(f"PET BRAIN listening on ws://{host}:{port}")
            await asyncio.Future()
    finally:
        behavior_task.cancel()
        await asyncio.gather(behavior_task, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(run_server())
