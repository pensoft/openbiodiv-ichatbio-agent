"""
Main entry point for the OpenBiodiv Agent
"""

from ichatbio.server import build_agent_app
from .openbiodiv_agent import OpenBiodivAgent
from starlette.applications import Starlette
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
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
    api_base_url = os.getenv("OPENBIODIV_API_URL", "https://api.openbiodiv.net")

    logger.info(f"Creating OpenBiodiv Agent application")
    logger.info(f"Using OpenBiodiv API: {api_base_url}")

    agent = OpenBiodivAgent(api_base_url=api_base_url)
    return build_agent_app(agent)


if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "9999"))
    api_base_url = os.getenv("OPENBIODIV_API_URL", "https://api.openbiodiv.net")

    logger.info("=" * 60)
    logger.info("Starting OpenBiodiv iChatBio Agent")
    logger.info("=" * 60)
    logger.info(f"Server Address: http://{host}:{port}")
    logger.info(f"OpenBiodiv API: {api_base_url}")
    logger.info(f"Agent Card: http://{host}:{port}/.well-known/agent.json")
    logger.info("=" * 60)

    # Create and run the agent
    app = create_app()
    uvicorn.run(app, host=host, port=port)
