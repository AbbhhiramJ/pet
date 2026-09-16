import json
import time

from pet_brain.models import PetEvent
from pet_brain.personality import PersonalityEngine

def event(name: str, value=None) -> PetEvent:
    return PetEvent(type="event", event=name, timestamp=time.time(), value=value)

def run_demo() -> None:
    engine = PersonalityEngine()
    print("OFFLINE AI PET — SIMULATOR")
    print(json.dumps(engine.snapshot(), indent=2))
    for name in ("motion", "touch", "voice", "touch"):
        evt = event(name)
        print(f"\nESP32 → MAC: {evt.model_dump_json()}")
        for command in engine.handle(evt.event):
            print(f"MAC → ESP32: {json.dumps({**command, 'type':'command'})}")
        print(f"STATE: {json.dumps(engine.snapshot())}")

if __name__ == "__main__": run_demo()
