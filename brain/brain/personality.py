from dataclasses import dataclass


@dataclass
class PetState:
    energy: float = 80.0
    happiness: float = 70.0
    curiosity: float = 60.0
    affection: float = 50.0
    boredom: float = 20.0
    sleepiness: float = 10.0

    def clamp(self) -> None:
        for field in ("energy", "happiness", "curiosity", "affection", "boredom", "sleepiness"):
            setattr(self, field, max(0.0, min(100.0, getattr(self, field))))

    @property
    def mood(self) -> str:
        if self.sleepiness >= 75 or self.energy <= 15:
            return "sleepy"
        if self.happiness >= 75:
            return "happy"
        if self.boredom >= 75:
            return "bored"
        if self.affection >= 75:
            return "affectionate"
        return "neutral"


class PersonalityEngine:
    """Deterministic V1 behavior. The LLM is deliberately not in this loop."""

    def __init__(self, state: PetState | None = None) -> None:
        self.state = state or PetState()

    def tick(self, minutes: float = 1.0) -> None:
        self.state.boredom += 0.4 * minutes
        self.state.energy -= 0.08 * minutes
        self.state.sleepiness += 0.12 * minutes
        self.state.clamp()

    def handle(self, event: str) -> list[dict]:
        if event == "touch":
            self.state.affection += 5
            self.state.happiness += 4
            self.state.boredom -= 4
            self.state.energy -= 0.5
            self.state.clamp()
            return [{"command": "set_expression", "expression": "happy"}]

        if event == "motion":
            self.state.curiosity += 3
            self.state.boredom -= 2
            self.state.clamp()
            return [{"command": "set_expression", "expression": "curious"}]

        if event == "voice":
            self.state.curiosity += 2
            self.state.affection += 1
            self.state.boredom -= 3
            self.state.clamp()
            return [{"command": "set_expression", "expression": "listening"}]

        return []

    def snapshot(self) -> dict[str, float | str]:
        return {
            "energy": round(self.state.energy, 1),
            "happiness": round(self.state.happiness, 1),
            "curiosity": round(self.state.curiosity, 1),
            "affection": round(self.state.affection, 1),
            "boredom": round(self.state.boredom, 1),
            "sleepiness": round(self.state.sleepiness, 1),
            "mood": self.state.mood,
        }
