import asyncio

from websockets.asyncio.client import connect

from pet_brain.models import PetEvent
from pet_brain.protocol import new_id, now

URL = "ws://127.0.0.1:8765"
EVENTS = {"touch", "motion", "voice", "orientation", "battery", "heartbeat"}


def make_event(name: str) -> str:
    return PetEvent(event=name, event_id=new_id("evt"), timestamp=now()).model_dump_json()


async def receive_messages(ws) -> None:
    try:
        async for message in ws:
            print("MAC -> ESP32:", message, flush=True)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        print(f"Receiver stopped: {exc}", flush=True)


async def main() -> None:
    async with connect(URL) as ws:
        print("VIRTUAL ESP32 connected")
        print("Type: touch | motion | voice | orientation | battery | heartbeat | quit")

        receiver_task = asyncio.create_task(receive_messages(ws))
        try:
            while True:
                name = (await asyncio.to_thread(input, "ESP32> ")).strip().lower()
                if name == "quit":
                    break
                if not name:
                    continue
                if name not in EVENTS:
                    print("Unknown event")
                    continue
                await ws.send(make_event(name))
        finally:
            receiver_task.cancel()
            await asyncio.gather(receiver_task, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
