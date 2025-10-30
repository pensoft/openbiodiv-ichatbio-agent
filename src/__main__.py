"""
Execute the OpenBiodiv Agent as a package.

Usage:
    python -m src
"""

from .agent import create_app
import uvicorn
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration with defaults
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
AGENT_URL = os.getenv("AGENT_URL")
AGENT_ICON_URL = os.getenv("AGENT_ICON_URL")
OPENBIODIV_API_URL = os.getenv("OPENBIODIV_API_URL")
API_TIMEOUT = int(os.getenv("API_TIMEOUT"))
LOG_LEVEL = os.getenv("LOG_LEVEL")

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting OpenBiodiv iChatBio Agent")
    logger.info("=" * 60)
    logger.info(f"Agent URL: {AGENT_URL}")
    logger.info(f"OpenBiodiv API: {OPENBIODIV_API_URL}")
    logger.info(f"Agent Card: {AGENT_URL}/.well-known/agent.json")
    logger.info(f"Server: {HOST}:{PORT}")
    logger.info("=" * 60)

    # Create and run the agent
    app = create_app(
        api_base_url=OPENBIODIV_API_URL,
        agent_url=AGENT_URL,
        agent_icon_url=AGENT_ICON_URL,
        api_timeout=API_TIMEOUT
    )
    uvicorn.run(app, host=HOST, port=PORT)
