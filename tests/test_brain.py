from pathlib import Path
from tempfile import TemporaryDirectory

from pet_brain.behavior import BehaviorEngine
from pet_brain.brain import PetBrain
from pet_brain.llm import OllamaClient
from pet_brain.memory import LocalMemory
from pet_brain.models import PetInteraction
from pet_brain.personality import PetState


class FailingLLM(OllamaClient):
    def chat_json(self, system: str, user: str) -> dict:
        raise RuntimeError("offline")


def make_brain() -> PetBrain:
    tmp = TemporaryDirectory()
    memory = LocalMemory(Path(tmp.name) / "memory.json")
    brain = PetBrain(BehaviorEngine(PetState()), FailingLLM(), memory)
    brain._tmp = tmp
    return brain


def test_brain_falls_back_offline_and_handles_affection() -> None:
    brain = make_brain()
    result = brain.handle_text("I love you, pet")
    assert result.intent == "affection"
    assert result.actions[-1]["expression"] == "happy"
    assert result.reply == "I like that."


def test_brain_status_does_not_send_hardware_command() -> None:
    brain = make_brain()
    result = brain.handle_text("how are you")
    assert result.intent == "status"
    assert result.actions == []
    assert "neutral" in result.reply


def test_memory_persists_recent_messages() -> None:
    with TemporaryDirectory() as directory:
        path = Path(directory) / "memory.json"
        memory = LocalMemory(path)
        memory.add("user", "hello")
        memory.add("pet", "Hello.")
        reloaded = LocalMemory(path)
        assert reloaded.recent() == [
            {"role": "user", "content": "hello"},
            {"role": "pet", "content": "Hello."},
        ]


def test_interaction_message_accepts_natural_language() -> None:
    interaction = PetInteraction(type="interaction", text="I love you")
    assert interaction.text == "I love you"
