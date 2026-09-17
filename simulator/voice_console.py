import argparse
import asyncio
import json

from websockets.asyncio.client import connect

from pet_brain.speech import SpeechConfig, WhisperSpeech

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
    parser = argparse.ArgumentParser(description="Local microphone console for the AI pet")
    parser.add_argument("--seconds", type=float, default=5.0, help="seconds to record per turn")
    parser.add_argument("--model", default="base", help="local Whisper model name")
    parser.add_argument("--language", default=None, help="optional language code, e.g. en")
    args = parser.parse_args()

    speech = WhisperSpeech(SpeechConfig(model=args.model, language=args.language))

    async with connect(URL) as ws:
        print("VOICE CONSOLE connected")
        print("Press Enter to record. Type 'quit' to exit.")
        receiver_task = asyncio.create_task(receive_messages(ws))
        try:
            while True:
                command = (await asyncio.to_thread(input, "VOICE> ")).strip()
                if command.lower() == "quit":
                    break
                print(f"Listening for {args.seconds:g} seconds...", flush=True)
                text = await asyncio.to_thread(speech.listen_once, args.seconds)
                if not text:
                    print("No speech detected.", flush=True)
                    continue
                print(f"YOU: {text}", flush=True)
                await ws.send(json.dumps({"type": "interaction", "text": text}))
        finally:
            receiver_task.cancel()
            await asyncio.gather(receiver_task, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
