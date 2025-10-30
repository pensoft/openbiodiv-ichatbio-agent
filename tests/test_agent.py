import pytest
from unittest.mock import patch
from src.agent import OpenBiodivAgent
from src.agent_card import (
    TaxonSearchParams,
    GeneralSearchParams,
    UUIDParams
)


class TestOpenBiodivAgent:
    """Test suite for OpenBiodiv iChatBio Agent"""

    @pytest.fixture
    def agent(self):
        """Create an OpenBiodivAgent instance"""
        return OpenBiodivAgent(
            api_base_url="https://api.openbiodiv.net",
            agent_url="http://localhost:9999",
            icon_url="https://openbiodiv.net/favicon.ico",
            api_timeout=30
        )

    def test_agent_card(self, agent):
        """Test that agent card contains correct metadata and all entrypoints"""
        card = agent.get_agent_card()

        assert card.name == "OpenBiodiv Agent"
        assert "biodiversity knowledge" in card.description.lower()
        assert len(card.entrypoints) == 18

        # Verify key entrypoints exist
        entrypoint_ids = [ep.id for ep in card.entrypoints]
        assert "search" in entrypoint_ids
        assert "search_taxons" in entrypoint_ids
        assert "get_article" in entrypoint_ids
        assert "get_by_uuid" in entrypoint_ids

    @pytest.mark.asyncio
    async def test_search_taxons(self, agent, context, messages):
        """Test taxon search with mocked API response"""

        # Mock the client's search_taxons method
        mock_response = {
            "count": 2,
            "taxons": [
                {
                    "id": "taxon-123",
                    "scientificName": "Apis mellifera",
                    "rank": "species",
                    "kingdom": "Animalia"
                },
                {
                    "id": "taxon-456",
                    "scientificName": "Apis cerana",
                    "rank": "species",
                    "kingdom": "Animalia"
                }
            ]
        }

        with patch.object(agent.client, 'search_taxons', return_value=mock_response):
            params = TaxonSearchParams(query="Apis", limit=10)

            await agent.run(
                context=context,
                request="Search for Apis taxons",
                entrypoint="search_taxons",
                params=params
            )

        # Verify agent sent a reply
        assert len(messages) > 0
        reply = messages[-1].text  # DirectResponse has a .text attribute
        assert "Apis" in reply or "taxon" in reply.lower()

    @pytest.mark.asyncio
    async def test_get_article(self, agent, context, messages):
        """Test article retrieval by UUID with mocked API response"""

        # Mock the client's get_article method
        mock_response = {
            "article": {
                "id": "article-789",
                "uuid": "12345678-1234-1234-1234-123456789abc",
                "title": "A new species of bee from Madagascar",
                "authors": ["Smith, J.", "Jones, A."],
                "publicationDate": "2023-05-15"
            }
        }

        with patch.object(agent.client, 'get_article', return_value=mock_response):
            params = UUIDParams(uuid="12345678-1234-1234-1234-123456789abc")

            await agent.run(
                context=context,
                request="Get article by UUID",
                entrypoint="get_article",
                params=params
            )

        # Verify agent sent a reply
        assert len(messages) > 0
        reply = messages[-1].text
        assert "article" in reply.lower() or "uuid" in reply.lower()

    @pytest.mark.asyncio
    async def test_general_search(self, agent, context, messages):
        """Test general search with mocked API response"""

        # Mock the client's search method
        mock_response = {
            "count": 5,
            "results": [
                {"type": "taxon", "name": "Apis mellifera", "id": "taxon-1"},
                {"type": "article", "title": "Bee diversity", "id": "article-1"},
                {"type": "treatment", "title": "Apis treatment", "id": "treatment-1"}
            ]
        }

        with patch.object(agent.client, 'search', return_value=mock_response):
            params = GeneralSearchParams(query="bee", limit=10)

            await agent.run(
                context=context,
                request="Search for bee",
                entrypoint="search",
                params=params
            )

        # Verify agent sent a reply
        assert len(messages) > 0
        reply = messages[-1].text
        assert "search" in reply.lower() or "result" in reply.lower()

    # Note: test_get_statistics removed as the statistics entrypoint doesn't exist in the current implementation

    @pytest.mark.asyncio
    async def test_error_handling(self, agent, context, messages):
        """Test that agent handles API errors gracefully"""

        # Mock the client to return an error response
        mock_error_response = {
            "error": "API connection failed",
            "results": []
        }

        with patch.object(agent.client, 'search_taxons', return_value=mock_error_response):
            params = TaxonSearchParams(query="test", limit=10)

            await agent.run(
                context=context,
                request="Search for test taxons",
                entrypoint="search_taxons",
                params=params
            )

        # Agent should still send a reply even on error
        assert len(messages) > 0
