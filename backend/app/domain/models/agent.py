from pydantic import BaseModel, Field
from typing import Optional
from app.domain.models.memory import Memory
import uuid

class Agent(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    planner_memory: Memory
    execution_memory: Memory
    model_name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
