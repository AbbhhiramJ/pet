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
        if self.sleepiness >= 75 or self.energy <= 15: return "sleepy"
        if self.happiness >= 75: return "happy"
        if self.boredom >= 75: return "bored"
        if self.affection >= 75: return "affectionate"
        return "neutral"

class PersonalityEngine:
    def __init__(self, state: PetState | None = None) -> None:
        self.state = state or PetState()

    def tick(self, minutes: float = 1.0) -> None:
        self.state.boredom += 0.4 * minutes
        self.state.energy -= 0.08 * minutes
        self.state.sleepiness += 0.12 * minutes
        self.state.clamp()

    def handle(self, event: str) -> list[dict]:
        changes = {"touch": (5,4,0, -4,-0.5,"happy"), "motion": (0,0,3,-2,0,"curious"), "voice": (0,0,2,-3,0,"listening")}
        if event not in changes: return []
        aff, happy, cur, bored, energy, expression = changes[event]
        self.state.affection += aff; self.state.happiness += happy; self.state.curiosity += cur; self.state.boredom += bored; self.state.energy += energy
        self.state.clamp()
        return [{"command":"set_expression", "expression":expression}]

    def snapshot(self) -> dict[str, float | str]:
        return {k: round(getattr(self.state,k),1) for k in ("energy","happiness","curiosity","affection","boredom","sleepiness")} | {"mood": self.state.mood}
