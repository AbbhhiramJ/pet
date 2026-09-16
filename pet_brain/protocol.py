import time
import uuid

def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def now() -> float:
    return time.time()
