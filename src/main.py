"""
Main entry point for the OpenBiodiv Agent
"""

from ichatbio.server import build_agent_app
from .agent import OpenBiodivAgent
from starlette.applications import Starlette
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Agent configuration
AGENT_URL = os.getenv("AGENT_URL", "http://localhost:9999")
AGENT_ICON_URL = os.getenv("AGENT_ICON_URL", "https://openbiodiv.net/favicon.ico")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# OpenBiodiv API configuration
OPENBIODIV_API_URL = os.getenv("OPENBIODIV_API_URL", "https://api.openbiodiv.net")

# Timeout configuration (in seconds)
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
ARCHIVE_TIMEOUT = int(os.getenv("ARCHIVE_TIMEOUT", "60"))

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def create_app() -> Starlette:
    """
    Factory function to create the agent application

    Returns:
        Starlette application instance with the OpenBiodiv agent
    """
    logger.info(f"Creating OpenBiodiv Agent application")
    logger.info(f"Using OpenBiodiv API: {OPENBIODIV_API_URL}")
    logger.info(f"Agent URL: {AGENT_URL}")

    agent = OpenBiodivAgent(
        api_base_url=OPENBIODIV_API_URL,
        agent_url=AGENT_URL,
        icon_url=AGENT_ICON_URL,
        api_timeout=API_TIMEOUT,
        archive_timeout=ARCHIVE_TIMEOUT
    )
    return build_agent_app(agent)