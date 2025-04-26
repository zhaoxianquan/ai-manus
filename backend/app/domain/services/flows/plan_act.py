import logging
from app.domain.services.flows.base import BaseFlow
from app.domain.models.agent import Agent
from app.domain.models.event import AgentEvent
from typing import AsyncGenerator
from enum import Enum
from app.domain.models.event import (
    AgentEvent, 
    PlanCreatedEvent, 
    PlanCompletedEvent,
    DoneEvent
)
from app.domain.models.plan import ExecutionStatus
from app.domain.services.agents.planner import PlannerAgent
from app.domain.services.agents.execution import ExecutionAgent
from app.domain.external.llm import LLM
from app.domain.external.sandbox import Sandbox
from app.domain.external.browser import Browser
from app.domain.external.search import SearchEngine

logger = logging.getLogger(__name__)

class AgentStatus(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    UPDATING = "updating"

class PlanActFlow(BaseFlow):
    def __init__(self, agent: Agent, llm: LLM, sandbox: Sandbox, browser: Browser, search_engine: SearchEngine):
        super().__init__(agent)
        self.status = AgentStatus.IDLE
        self.plan = None
        # 创建计划代理和执行代理
        self.planner = PlannerAgent(
            llm=llm,
            memory=agent.planner_memory,
        )
        logger.debug(f"Created planner agent for Agent {self.agent.id}")
        
        self.executor = ExecutionAgent(
            llm=llm,
            memory=agent.execution_memory,
            sandbox=sandbox,
            browser=browser,
            search_engine=search_engine,
        )
        logger.debug(f"Created execution agent for Agent {self.agent.id}")

        

    async def run(self, message: str) -> AsyncGenerator[AgentEvent, None]:
        if not self.is_idle():
            # interrupt the current flow
            self.status = AgentStatus.PLANNING
            self.planner.roll_back()
            self.executor.roll_back()

        logger.info(f"Agent {self.agent.id} started processing message: {message[:50]}...")
        step = None
        while True:
            if self.status == AgentStatus.IDLE:
                logger.info(f"Agent {self.agent.id} state changed from {AgentStatus.IDLE} to {AgentStatus.PLANNING}")
                self.status = AgentStatus.PLANNING
            elif self.status == AgentStatus.PLANNING:
                # 创建计划
                logger.info(f"Agent {self.agent.id} started creating plan")
                async for event in self.planner.create_plan(message):
                    if isinstance(event, PlanCreatedEvent):
                        self.plan = event.plan
                        logger.info(f"Agent {self.agent.id} created plan successfully with {len(event.plan.steps)} steps")
                    yield event
                logger.info(f"Agent {self.agent.id} state changed from {AgentStatus.PLANNING} to {AgentStatus.EXECUTING}")
                self.status = AgentStatus.EXECUTING
                    
            elif self.status == AgentStatus.EXECUTING:
                # 执行计划
                self.plan.status = ExecutionStatus.RUNNING
                step = self.plan.get_next_step()
                if not step:
                    logger.info(f"Agent {self.agent.id} has no more steps, state changed from {AgentStatus.EXECUTING} to {AgentStatus.COMPLETED}")
                    self.status = AgentStatus.COMPLETED
                    continue
                # 执行步骤
                logger.info(f"Agent {self.agent.id} started executing step {step.id}: {step.description[:50]}...")
                async for event in self.executor.execute_step(self.plan, step):
                    yield event
                logger.info(f"Agent {self.agent.id} completed step {step.id}, state changed from {AgentStatus.EXECUTING} to {AgentStatus.UPDATING}")
                self.status = AgentStatus.UPDATING
            elif self.status == AgentStatus.UPDATING:
                # 更新计划
                logger.info(f"Agent {self.agent.id} started updating plan")
                async for event in self.planner.update_plan(self.plan):
                    yield event
                logger.info(f"Agent {self.agent.id} plan update completed, state changed from {AgentStatus.UPDATING} to {AgentStatus.EXECUTING}")
                self.status = AgentStatus.EXECUTING
            elif self.status == AgentStatus.COMPLETED:
                self.plan.status = ExecutionStatus.COMPLETED
                logger.info(f"Agent {self.agent.id} plan has been completed")
                yield PlanCompletedEvent(plan=self.plan) 
                self.status = AgentStatus.IDLE
                break
        yield DoneEvent()
        
        logger.info(f"Agent {self.agent.id} message processing completed")
    
    def is_idle(self) -> bool:
        return self.status == AgentStatus.IDLE