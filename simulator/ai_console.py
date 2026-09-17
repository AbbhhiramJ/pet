import asyncio
import json

from websockets.asyncio.client import connect

URL = "ws://127.0.0.1:8765"


async def receive_messages(ws) -> None:
    try:
        async for message in ws:
            payload = json.loads(message)
            message_type = payload.get("type")
            if message_type == "reply":
                print(f"PET: {payload['reply']} [{payload['intent']}]", flush=True)
            elif message_type == "command":
                print(f"MAC -> ESP32: {message}", flush=True)
            elif message_type == "state":
                print(f"STATE: {payload['state']}", flush=True)
            else:
                print(f"SERVER: {message}", flush=True)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        print(f"Receiver stopped: {exc}", flush=True)


async def main() -> None:
    async with connect(URL) as ws:
        print("AI CONSOLE connected")
        print("Type natural language. Type 'quit' to exit.")
        receiver_task = asyncio.create_task(receive_messages(ws))
        try:
            while True:
                text = (await asyncio.to_thread(input, "YOU> ")).strip()
                if text.lower() == "quit":
                    break
                if not text:
                    continue
                await ws.send(json.dumps({"type": "interaction", "text": text}))
        finally:
            receiver_task.cancel()
            await asyncio.gather(receiver_task, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
