import asyncio

from websockets.asyncio.client import connect

from pet_brain.models import PetEvent
from pet_brain.protocol import new_id, now

URL = "ws://127.0.0.1:8765"
EVENTS = {"touch", "motion", "voice", "orientation", "battery", "heartbeat"}

def make_event(name: str) -> str:
    return PetEvent(event=name, event_id=new_id("evt"), timestamp=now()).model_dump_json()

async def main() -> None:
    async with connect(URL) as ws:
        print("VIRTUAL ESP32 connected")
        print("Type: touch | motion | voice | orientation | battery | heartbeat | quit")
        while True:
            name = (await asyncio.to_thread(input, "ESP32> ")).strip().lower()
            if name == "quit":
                break
            if name not in EVENTS:
                print("Unknown event")
                continue
            await ws.send(make_event(name))
            try:
                while True:
                    print("MAC -> ESP32:", await asyncio.wait_for(ws.recv(), timeout=0.15))
            except asyncio.TimeoutError:
                pass

if __name__ == "__main__":
    asyncio.run(main())
