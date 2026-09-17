from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

EventName = Literal["touch", "motion", "orientation", "voice", "heartbeat", "battery"]
CommandName = Literal["set_expression", "move_servo", "play_sound", "set_led", "sleep", "wake", "heartbeat"]


class PetEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["event"] = "event"
    event: EventName
    event_id: str
    device_id: str = "virtual-esp32"
    timestamp: float
    value: Any | None = None
    data: dict[str, Any] | None = None


class PetInteraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["interaction"] = "interaction"
    text: str = Field(min_length=1, max_length=1000)


class PetCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["command"] = "command"
    command: CommandName
    command_id: str
    device_id: str = "virtual-esp32"
    timestamp: float
    expression: str | None = None
    servo: str | None = None
    angle: int | None = Field(default=None, ge=0, le=180)
    sound: str | None = None
    value: Any | None = None


class PetAck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["ack"] = "ack"
    message_id: str
    timestamp: float
    status: Literal["ok", "error"] = "ok"
    detail: str | None = None
