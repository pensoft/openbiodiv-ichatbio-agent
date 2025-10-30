# OpenBiodiv iChatBio Agent

An [Agent2Agent (A2A)](https://a2aprotocol.ai/) protocol-compliant agent that bridges OpenBiodiv's biodiversity knowledge graph with the iChatBio agent ecosystem.

## Overview

This agent provides access to the [OpenBiodiv](https://openbiodiv.net) database through the iChatBio platform, enabling AI agents to query biodiversity data including taxonomic information, scientific articles, treatments, specimens, genetic sequences, authors, and institutions.

## Features

- 🔍 **Comprehensive Search** - Query across all resource types or search specific categories
- 🦋 **Taxonomic Data** - Access scientific names, ranks, and classifications
- 📄 **Scientific Articles** - Search biodiversity literature
- 🔬 **Treatments** - Browse taxonomic treatments from publications
- 🏺 **Specimens** - Access specimen records and collection data
- 🧬 **Genetic Sequences** - Query DNA/RNA sequence data
- 👥 **Authors & Institutions** - Search researchers and organizations
- 📊 **Statistics** - Retrieve database metrics and counts
- 🔌 **A2A Protocol** - Full Agent2Agent protocol compliance for interoperability

## Quick Start

### Prerequisites

- Python 3.12 or 3.13
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Run with uv (recommended)

```bash
# Clone the repository
git clone <repository-url>
cd openbiodiv-ichatbio-agent

# Install dependencies
uv sync

# Run the agent (recommended)
uv run python -m src
```

### Run with Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t openbiodiv-agent .
docker run -p 9999:9999 \
  -e AGENT_URL=http://localhost:9999\
  -e AGENT_ICON_URL=https://openbiodiv.net/favicon.ico \
  -e LOG_LEVEL=DEBUG \
  openbiodiv-agent
```

The agent will be available at `http://localhost:9999`

## Installation

### Using uv (recommended)

```bash
# Create virtual environment and install dependencies
uv sync

# Install development dependencies
uv sync --extra dev
```

### Using pip

```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

## Usage

### Local Development

```bash
# Run the agen
uv run python -m src

# With custom configuration
HOST=127.0.0.1 PORT=8080 uv run python -m src
```

### Docker Compose

```bash
# Start the agent
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the agent
docker-compose down
```

### Verify Installation

Once running, verify the agent is working:

```bash
# Check agent card
curl http://localhost:9999/.well-known/agent.json

# Health check
curl http://localhost:9999/health
```

## Available Entrypoints

The agent provides 19 entrypoints organized by resource type:

### General

- `search` - Search across all resource types

### Taxons

- `search_taxons` - Search taxonomic information
- `get_taxon` - Get taxon details by UUID

### Articles

- `search_articles` - Search scientific articles
- `get_article` - Get article details by UUID

### Treatments

- `search_treatments` - Search taxonomic treatments
- `get_treatment` - Get treatment details by UUID

### Specimens

- `search_specimens` - Search specimen records
- `get_specimen` - Get specimen details by UUID

### Authors

- `search_authors` - Search authors
- `get_author` - Get author details by UUID

### Institutions

- `search_institutions` - Search institutions
- `get_institution` - Get institution details by UUID

### Sequences

- `search_sequences` - Search genetic sequences
- `get_sequence` - Get sequence details by UUID

### Sections

- `search_sections` - Search article sections
- `get_section` - Get section details by UUID

### Generic

- `get_by_uuid` - Get any resource by UUID

Full API documentation is available through the agent card at `/.well-known/agent.json`

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_openbiodiv_client.py
```

### Project Structure

```text
.
├── src/
│   ├── __init__.py
│   ├── __main__.py             # Package entry point (python -m src)
│   ├── agent_card.py           # Agent capabilities definition
│   ├── agent.py                # Agent implementation
│   └── client.py               # OpenBiodiv API client
├── tests/
│   ├── conftest.py             # Test fixtures
│   └── test_agent.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Integration with iChatBio

This agent is designed to work with the [iChatBio platform](https://github.com/acislab/ichatbio-sdk). Once deployed, other A2A-compliant agents can discover and interact with it through the standard A2A protocol.

To register this agent with iChatBio:

1. Deploy the agent to a publicly accessible URL
2. Update the `url` field in [agent_card.py](src/agent_card.py)
3. Register the agent card URL with the iChatBio platform

## About OpenBiodiv

[OpenBiodiv](https://openbiodiv.net) is a biodiversity knowledge graph based on RDF that contains information extracted from scientific literature. It provides comprehensive data on:

- Taxonomic nomenclature and classifications
- Biodiversity treatments from scientific publications
- Specimen records and collection data
- Genetic sequence information
- Author and institutional affiliations
- Scientific article metadata

Learn more at [openbiodiv.net](https://openbiodiv.net)
