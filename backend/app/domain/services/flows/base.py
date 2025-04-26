from app.domain.models.event import AgentEvent
from app.domain.models.agent import Agent
from typing import AsyncGenerator
from abc import ABC, abstractmethod
class BaseFlow(ABC):
    def __init__(self, agent: Agent):
        self.agent = agent

    @abstractmethod
    def run(self) -> AsyncGenerator[AgentEvent, None]:
        pass
