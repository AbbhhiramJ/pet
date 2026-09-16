import asyncio
import json
import time

from websockets.asyncio.client import connect

from brain.models import PetEvent

URL = "ws://127.0.0.1:8765"


def make_event(name: str) -> str:
    return PetEvent(type="event", event=name, timestamp=time.time()).model_dump_json()


async def main() -> None:
    async with connect(URL) as ws:
        print("VIRTUAL ESP32 connected")
        print("Type: touch | motion | voice | orientation | battery | heartbeat | quit")
        while True:
            name = await asyncio.to_thread(input, "ESP32> ")
            if name == "quit":
                break
            if name not in {"touch", "motion", "voice", "orientation", "battery", "heartbeat"}:
                print("Unknown event")
                continue
            await ws.send(make_event(name))
            try:
                while True:
                    message = await asyncio.wait_for(ws.recv(), timeout=0.15)
                    print("MAC -> ESP32:", message)
            except asyncio.TimeoutError:
                pass


if __name__ == "__main__":
    asyncio.run(main())
