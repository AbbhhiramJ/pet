import json
import time

from brain.personality import PersonalityEngine
from brain.models import PetEvent


def event(name: str, value=None) -> PetEvent:
    return PetEvent(type="event", event=name, timestamp=time.time(), value=value)


def run_demo() -> None:
    engine = PersonalityEngine()
    print("OFFLINE AI PET — SIMULATOR")
    print("===========================")
    print(json.dumps(engine.snapshot(), indent=2))

    for name in ("motion", "touch", "voice", "touch"):
        evt = event(name)
        commands = engine.handle(evt.event)
        print(f"\nESP32 → MAC: {evt.model_dump_json()}")
        for command in commands:
            command["type"] = "command"
            print(f"MAC → ESP32: {json.dumps(command)}")
        print(f"STATE: {json.dumps(engine.snapshot())}")


if __name__ == "__main__":
    run_demo()
