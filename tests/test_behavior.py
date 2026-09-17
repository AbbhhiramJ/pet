from random import Random

from pet_brain.behavior import BehaviorEngine
from pet_brain.personality import PetState


def test_sleep_when_energy_is_critical() -> None:
    engine = BehaviorEngine(PetState(energy=5.0, sleepiness=20.0), Random(1))
    actions = engine.tick()
    assert actions == [{"command": "sleep", "reason": "low_energy_or_high_sleepiness"}]
    assert engine.awake is False


def test_wake_after_rest() -> None:
    engine = BehaviorEngine(PetState(energy=34.0, sleepiness=26.0), Random(1))
    engine.awake = False
    engine.state.sleepiness = 26.0
    engine.state.energy = 34.0
    actions = engine.tick(3)
    assert actions == [{"command": "wake", "reason": "rested"}]
    assert engine.awake is True


def test_idle_can_be_deterministic() -> None:
    state = PetState(boredom=100.0)
    engine = BehaviorEngine(state, Random(1))
    assert engine.idle()[0]["reason"] == "bored_idle"


def test_sleeping_pet_does_not_idle() -> None:
    engine = BehaviorEngine(PetState(), Random(1))
    engine.awake = False
    assert engine.idle() == []


def test_expression_tracks_mood() -> None:
    state = PetState(happiness=90.0)
    engine = BehaviorEngine(state, Random(1))
    assert engine.expression_for_mood() == "happy"
