import json

from pet_brain.models import PetAck, PetCommand, PetEvent
from pet_brain.protocol import new_id, now

def test_event_round_trip() -> None:
    event = PetEvent(event="touch", event_id=new_id("evt"), timestamp=now())
    restored = PetEvent.model_validate_json(event.model_dump_json())
    assert restored.event == "touch"
    assert restored.event_id == event.event_id

def test_command_id_and_validation() -> None:
    command = PetCommand(command="move_servo", command_id=new_id("cmd"), timestamp=now(), servo="head", angle=90)
    assert command.command_id.startswith("cmd_")
    assert command.angle == 90

def test_ack() -> None:
    ack = PetAck(message_id="evt_123", timestamp=now())
    assert ack.status == "ok"

def test_extra_fields_rejected() -> None:
    payload = {"type":"event","event":"touch","event_id":"evt_1","device_id":"esp32","timestamp":1,"unexpected":True}
    try:
        PetEvent.model_validate(payload)
    except Exception:
        return
    raise AssertionError("Unexpected fields must be rejected")
