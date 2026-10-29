
# ==========================================
# 1. TypedDict: State ka structure define karna
# ==========================================

from typing import TypedDict

class TypedDictState(TypedDict):
    # Topic ka data string hoga
    topic: str

    # Summary ka data string hoga
    summary: str

    # Score integer hoga
    score: int


# ==========================================
# 2. Pydantic: Data ko validate karna
# ==========================================

from pydantic import BaseModel, field_validator

class PydanticState(BaseModel):
    topic: str
    summary: str
    score: int

    # Sirf score field ke liye validation
    @field_validator("score")
    @classmethod
    def validate_score(cls, value: int) -> int:
        # Score 0 se 100 ke darmiyan hona chahiye
        if not (0 <= value <= 100):
            raise ValueError("Score must be between 0 and 100")

        # Valid score return kar do
        return value


# ==========================================
# 3. Dataclass: Data ko organize karna
# ==========================================

from dataclasses import dataclass, field

@dataclass
class DataclassState:
    topic: str
    summary: str

    # Har object ki apni separate empty list hogi
    messages: list = field(default_factory=list)


# ==========================================
# 4. MessagesState: Chat messages manage karna
# ==========================================

from langgraph.graph import MessagesState

class ChatState(MessagesState):
    # MessagesState pehle se messages field provide karta hai
    # Hum apni additional fields add kar rahe hain
    username: str
    language: str
