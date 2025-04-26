from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.interfaces.api.routes import router
from app.application.services.agent import AgentService
from app.infrastructure.config import get_settings
from app.infrastructure.logging import setup_logging
from app.interfaces.api.errors.exception_handlers import register_exception_handlers

# Initialize logging system
setup_logging()
logger = logging.getLogger(__name__)

# Load configuration
settings = get_settings()

# Create lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code executed on startup
    logger.info("Application startup - Manus AI Agent initializing")
    yield
    # Code executed on shutdown
    logger.info("Application shutdown - Manus AI Agent terminating")
    await agent_service.close()

app = FastAPI(title="Manus AI Agent", lifespan=lifespan)
agent_service = AgentService()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
register_exception_handlers(app)

# Register routes
app.include_router(router, prefix="/api/v1")