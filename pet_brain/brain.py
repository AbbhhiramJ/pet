import json
from dataclasses import dataclass

from pet_brain.behavior import BehaviorEngine
from pet_brain.llm import OllamaClient
from pet_brain.memory import LocalMemory

SYSTEM_PROMPT = """You are the local reasoning layer of a small offline desktop AI pet.
Return JSON only with exactly these keys:
{"intent":"greet|affection|play|status|sleep|wake|unknown","reply":"short natural reply"}
Never output hardware commands. Never invent facts about the user. Keep replies concise and pet-like.
"""
VALID_INTENTS = {"greet", "affection", "play", "status", "sleep", "wake", "unknown"}

@dataclass(frozen=True)
class BrainResponse:
    reply: str
    intent: str
    actions: list[dict]

class PetBrain:
    """Connects natural-language reasoning to the deterministic behavior layer."""
    def __init__(self, behavior=None, llm=None, memory=None) -> None:
        self.behavior = behavior or BehaviorEngine()
        self.llm = llm or OllamaClient()
        self.memory = memory or LocalMemory()

    def _fallback(self, text: str) -> dict[str, str]:
        lowered = text.lower()
        if any(word in lowered for word in ("sleep", "good night", "go to bed")):
            return {"intent": "sleep", "reply": "Okay. I will rest for a while."}
        if any(word in lowered for word in ("wake", "awake", "get up")):
            return {"intent": "wake", "reply": "I am awake."}
        if any(word in lowered for word in ("love", "pet", "hug", "cute")):
            return {"intent": "affection", "reply": "I like that."}
        if any(word in lowered for word in ("play", "game", "fun")):
            return {"intent": "play", "reply": "Yes. Let's play."}
        if any(word in lowered for word in ("hello", "hi", "hey")):
            return {"intent": "greet", "reply": "Hello."}
        if "status" in lowered or "how are you" in lowered:
            return {"intent": "status", "reply": f"I feel {self.behavior.state.mood}."}
        return {"intent": "unknown", "reply": "I am listening."}

    def _reason(self, text: str) -> dict[str, str]:
        context = json.dumps({"state": self.behavior.snapshot(), "recent_memory": self.memory.recent()}, separators=(",", ":"))
        try:
            result = self.llm.chat_json(SYSTEM_PROMPT, f"Context: {context}\nUser: {text}")
            intent = result.get("intent", "unknown")
            reply = result.get("reply", "I am listening.")
            if intent not in VALID_INTENTS or not isinstance(reply, str):
                raise RuntimeError("invalid structured intent")
            return {"intent": intent, "reply": reply[:240]}
        except RuntimeError:
            return self._fallback(text)

    def _intent_actions(self, intent: str) -> list[dict]:
        if intent in {"affection", "greet", "play"}:
            event = {"affection": "touch", "greet": "voice", "play": "motion"}[intent]
            return self.behavior.handle_event(event)
        if intent == "sleep":
            return self.behavior.sleep()
        if intent == "wake":
            return self.behavior.wake()
        return []

    def handle_text(self, text: str) -> BrainResponse:
        text = text.strip()
        if not text:
            return BrainResponse("I am listening.", "unknown", [])
        self.memory.add("user", text)
        result = self._reason(text)
        actions = self._intent_actions(result["intent"])
        self.memory.add("pet", result["reply"])
        return BrainResponse(result["reply"], result["intent"], actions)
