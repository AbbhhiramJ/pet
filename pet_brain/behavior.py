from dataclasses import dataclass
import random

from pet_brain.personality import PetState


@dataclass(frozen=True)
class BehaviorAction:
    command: str
    expression: str | None = None
    sound: str | None = None
    reason: str | None = None


class BehaviorEngine:
    """Deterministic high-level behavior layer for the offline pet."""

    def __init__(self, state: PetState | None = None, rng: random.Random | None = None) -> None:
        self.state = state or PetState()
        self.rng = rng or random.Random()
        self.awake = True

    def tick(self, minutes: float = 1.0) -> list[dict]:
        if minutes < 0:
            raise ValueError("minutes must be non-negative")
        if self.awake:
            self.state.boredom += 0.4 * minutes
            self.state.energy -= 0.08 * minutes
            self.state.sleepiness += 0.12 * minutes
            self.state.clamp()
            if self.state.sleepiness >= 90 or self.state.energy <= 5:
                return self.sleep()
        else:
            self.state.energy += 0.35 * minutes
            self.state.sleepiness -= 0.5 * minutes
            self.state.boredom += 0.05 * minutes
            self.state.clamp()
            if self.state.sleepiness <= 25 and self.state.energy >= 35:
                return self.wake()
        return []

    def sleep(self) -> list[dict]:
        self.awake = False
        return [{"command": "sleep", "reason": "low_energy_or_high_sleepiness"}]

    def wake(self) -> list[dict]:
        self.awake = True
        self.state.sleepiness = min(self.state.sleepiness, 20.0)
        return [{"command": "wake", "reason": "rested"}]

    def idle(self) -> list[dict]:
        if not self.awake:
            return []
        if self.state.boredom < 45 or self.rng.random() > 0.20:
            return []
        choices = [
            {"command": "set_expression", "expression": "curious", "reason": "bored_idle"},
            {"command": "set_expression", "expression": "happy", "reason": "bored_idle"},
            {"command": "play_sound", "sound": "chirp", "reason": "bored_idle"},
        ]
        return [self.rng.choice(choices)]

    def expression_for_mood(self) -> str:
        return {
            "sleepy": "sleepy",
            "happy": "happy",
            "bored": "bored",
            "affectionate": "love",
            "neutral": "neutral",
        }[self.state.mood]

    def snapshot(self) -> dict:
        return {
            "awake": self.awake,
            "mood": self.state.mood,
            "expression": self.expression_for_mood(),
            "energy": round(self.state.energy, 1),
            "happiness": round(self.state.happiness, 1),
            "curiosity": round(self.state.curiosity, 1),
            "affection": round(self.state.affection, 1),
            "boredom": round(self.state.boredom, 1),
            "sleepiness": round(self.state.sleepiness, 1),
        }
