"""
Execute the OpenBiodiv Agent as a package.

Usage:
    python -m src
"""

from .main import create_app
import uvicorn
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "9999"))
AGENT_URL = os.getenv("AGENT_URL", f"http://localhost:{PORT}")
OPENBIODIV_API_URL = os.getenv("OPENBIODIV_API_URL", "https://api.openbiodiv.net")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting OpenBiodiv iChatBio Agent")
    logger.info("=" * 60)
    logger.info(f"Agent URL: {AGENT_URL}")
    logger.info(f"OpenBiodiv API: {OPENBIODIV_API_URL}")
    logger.info(f"Agent Card: {AGENT_URL}/.well-known/agent.json")
    logger.info("=" * 60)

    # Create and run the agent
    app = create_app()
    uvicorn.run(app, host=HOST, port=PORT)
