from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


EventName = Literal["touch", "motion", "orientation", "voice", "heartbeat", "battery"]
CommandName = Literal[
    "set_expression",
    "move_servo",
    "play_sound",
    "set_led",
    "sleep",
    "wake",
    "heartbeat",
]


class PetEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["event"]
    event: EventName
    timestamp: float
    value: Any | None = None
    data: dict[str, Any] | None = None


class PetCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["command"] = "command"
    command: CommandName
    expression: str | None = None
    servo: str | None = None
    angle: int | None = Field(default=None, ge=0, le=180)
    sound: str | None = None
    value: Any | None = None
