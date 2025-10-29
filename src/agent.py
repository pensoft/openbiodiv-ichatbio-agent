"""
OpenBiodiv Agent for the iChatBio framework
"""

from typing import override
from ichatbio.agent import IChatBioAgent
from ichatbio.agent_response import ResponseContext, IChatBioAgentProcess
from ichatbio.types import AgentCard
from .agent_card import (
    build_agent_card,
    GeneralSearchParams,
    TaxonSearchParams,
    ArticleSearchParams,
    TreatmentSearchParams,
    SpecimenSearchParams,
    AuthorSearchParams,
    InstitutionSearchParams,
    SequenceSearchParams,
    SectionSearchParams,
    UUIDParams
)
from .client import OpenBiodivClient
import json
import logging

logger = logging.getLogger(__name__)


class OpenBiodivAgent(IChatBioAgent):
    """iChatBio agent for querying OpenBiodiv biodiversity knowledge graph via REST API"""

    def __init__(
        self,
        api_base_url: str = "https://api.openbiodiv.net",
        agent_url: str = "http://localhost:9999",
        icon_url: str = "https://openbiodiv.net/favicon.ico",
        api_timeout: int = 30,
        archive_timeout: int = 60
    ):
        self.agent_url = agent_url
        self.icon_url = icon_url
        self.client = OpenBiodivClient(
            api_base_url=api_base_url,
            api_timeout=api_timeout,
            archive_timeout=archive_timeout
        )
        logger.info(f"OpenBiodiv Agent initialized with API: {api_base_url}")
        logger.info(f"Agent URL: {agent_url}")

    @override
    def get_agent_card(self) -> AgentCard:
        return build_agent_card(url=self.agent_url, icon=self.icon_url)

    @override
    async def run(
        self,
        context: ResponseContext,
        request: str,
        entrypoint: str,
        params: (GeneralSearchParams | TaxonSearchParams | ArticleSearchParams |
                TreatmentSearchParams | SpecimenSearchParams | AuthorSearchParams |
                InstitutionSearchParams | SequenceSearchParams | SectionSearchParams |
                UUIDParams)
    ):
        """Main execution method for handling different entrypoints"""

        async with context.begin_process(
            summary=f"Processing {entrypoint} request"
        ) as process:
            process: IChatBioAgentProcess

            try:
                # Route to appropriate handler based on entrypoint
                if entrypoint == "search":
                    await self._handle_general_search(process, context, params)

                elif entrypoint == "search_taxons":
                    await self._handle_taxon_search(process, context, params)
                elif entrypoint == "get_taxon":
                    await self._handle_get_taxon(process, context, params)

                elif entrypoint == "search_articles":
                    await self._handle_article_search(process, context, params)
                elif entrypoint == "get_article":
                    await self._handle_get_article(process, context, params)

                elif entrypoint == "search_treatments":
                    await self._handle_treatment_search(process, context, params)
                elif entrypoint == "get_treatment":
                    await self._handle_get_treatment(process, context, params)

                elif entrypoint == "search_specimens":
                    await self._handle_specimen_search(process, context, params)
                elif entrypoint == "get_specimen":
                    await self._handle_get_specimen(process, context, params)

                elif entrypoint == "search_authors":
                    await self._handle_author_search(process, context, params)
                elif entrypoint == "get_author":
                    await self._handle_get_author(process, context, params)

                elif entrypoint == "search_institutions":
                    await self._handle_institution_search(process, context, params)
                elif entrypoint == "get_institution":
                    await self._handle_get_institution(process, context, params)

                elif entrypoint == "search_sequences":
                    await self._handle_sequence_search(process, context, params)
                elif entrypoint == "get_sequence":
                    await self._handle_get_sequence(process, context, params)

                elif entrypoint == "search_sections":
                    await self._handle_section_search(process, context, params)
                elif entrypoint == "get_section":
                    await self._handle_get_section(process, context, params)

                elif entrypoint == "get_by_uuid":
                    await self._handle_get_by_uuid(process, context, params)

                else:
                    raise ValueError(f"Unknown entrypoint: {entrypoint}")

            except Exception as e:
                logger.error(f"Error in {entrypoint}: {e}", exc_info=True)
                await process.log(f"Error occurred: {str(e)}")
                await context.reply(
                    f"An error occurred while processing your request: {str(e)}"
                )

    # General Search Handler
    async def _handle_general_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: GeneralSearchParams
    ):
        """Handle general search across all resource types"""
        await process.log(f"Searching OpenBiodiv for: {params.query}")

        results = self.client.search(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"General search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Search completed for '{params.query}'. Results include various resource types from the OpenBiodiv database."
        await context.reply(summary)

    # Taxon Handlers
    async def _handle_taxon_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: TaxonSearchParams
    ):
        """Handle taxon search requests"""
        rank_info = f" (rank: {params.rank})" if params.rank else ""
        await process.log(f"Searching for taxon: {params.query}{rank_info}")

        results = self.client.search_taxons(query=params.query, rank=params.rank)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Taxon search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Taxon search results for '{params.query}'{rank_info}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found taxonomic information for '{params.query}'{rank_info}. Check the artifact for detailed results including taxonomy hierarchy."
        await context.reply(summary)

    async def _handle_get_taxon(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get taxon by UUID"""
        await process.log(f"Fetching taxon with UUID: {params.uuid}")

        results = self.client.get_taxon(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve taxon: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Taxon details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed taxon information for UUID {params.uuid}.")

    # Article Handlers
    async def _handle_article_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: ArticleSearchParams
    ):
        """Handle article search requests"""
        await process.log(f"Searching articles with query: {params.query}")

        results = self.client.search_articles(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Article search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Article search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found articles matching '{params.query}'. Results include titles, authors, DOIs, and keywords."
        await context.reply(summary)

    async def _handle_get_article(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get article by UUID"""
        await process.log(f"Fetching article with UUID: {params.uuid}")

        results = self.client.get_article(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve article: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Article details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed article information for UUID {params.uuid}.")

    # Treatment Handlers
    async def _handle_treatment_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: TreatmentSearchParams
    ):
        """Handle treatment search requests"""
        await process.log(f"Searching treatments with query: {params.query}")

        results = self.client.search_treatments(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Treatment search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Treatment search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found taxonomic treatments matching '{params.query}'."
        await context.reply(summary)

    async def _handle_get_treatment(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get treatment by UUID"""
        await process.log(f"Fetching treatment with UUID: {params.uuid}")

        results = self.client.get_treatment(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve treatment: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Treatment details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed treatment information for UUID {params.uuid}.")

    # Specimen Handlers
    async def _handle_specimen_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: SpecimenSearchParams
    ):
        """Handle specimen search requests"""
        await process.log(f"Searching specimens with query: {params.query}")

        results = self.client.search_specimens(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Specimen search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Specimen search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found specimen records matching '{params.query}'. Results include collection data, locality, and identification information."
        await context.reply(summary)

    async def _handle_get_specimen(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get specimen by UUID"""
        await process.log(f"Fetching specimen with UUID: {params.uuid}")

        results = self.client.get_specimen(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve specimen: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Specimen details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed specimen information for UUID {params.uuid}.")

    # Author Handlers
    async def _handle_author_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: AuthorSearchParams
    ):
        """Handle author search requests"""
        await process.log(f"Searching authors with query: {params.query}")

        results = self.client.search_authors(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Author search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Author search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found authors matching '{params.query}'. Results include publications, ORCID, and contact information."
        await context.reply(summary)

    async def _handle_get_author(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get author by UUID"""
        await process.log(f"Fetching author with UUID: {params.uuid}")

        results = self.client.get_author(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve author: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Author details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed author information for UUID {params.uuid}.")

    # Institution Handlers
    async def _handle_institution_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: InstitutionSearchParams
    ):
        """Handle institution search requests"""
        await process.log(f"Searching institutions with query: {params.query}")

        results = self.client.search_institutions(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Institution search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Institution search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found institutions matching '{params.query}'. Results include collection information and article mentions."
        await context.reply(summary)

    async def _handle_get_institution(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get institution by UUID"""
        await process.log(f"Fetching institution with UUID: {params.uuid}")

        results = self.client.get_institution(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve institution: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Institution details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed institution information for UUID {params.uuid}.")

    # Sequence Handlers
    async def _handle_sequence_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: SequenceSearchParams
    ):
        """Handle sequence search requests"""
        await process.log(f"Searching genetic sequences with query: {params.query}")

        results = self.client.search_sequences(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Sequence search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Sequence search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found genetic sequences matching '{params.query}'. Results include sequence mentions and collection data."
        await context.reply(summary)

    async def _handle_get_sequence(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get sequence by UUID"""
        await process.log(f"Fetching sequence with UUID: {params.uuid}")

        results = self.client.get_sequence(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve sequence: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Sequence details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed sequence information for UUID {params.uuid}.")

    # Section Handlers
    async def _handle_section_search(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: SectionSearchParams
    ):
        """Handle section search requests"""
        await process.log(f"Searching article sections with query: {params.query}")

        results = self.client.search_sections(query=params.query)

        if "error" in results:
            await process.log(f"Search failed: {results['error']}")
            await context.reply(f"Section search failed: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Section search results for '{params.query}'",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        summary = f"Found article sections matching '{params.query}'. Results include section hierarchy and parent information."
        await context.reply(summary)

    async def _handle_get_section(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get section by UUID"""
        await process.log(f"Fetching section with UUID: {params.uuid}")

        results = self.client.get_section(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve section: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Section details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        await context.reply(f"Retrieved detailed section information for UUID {params.uuid}.")

    # Generic UUID Handler
    async def _handle_get_by_uuid(
        self,
        process: IChatBioAgentProcess,
        context: ResponseContext,
        params: UUIDParams
    ):
        """Handle get resource by UUID (any type)"""
        await process.log(f"Fetching resource with UUID: {params.uuid}")

        results = self.client.get_by_uuid(uuid=params.uuid)

        if "error" in results:
            await process.log(f"Fetch failed: {results['error']}")
            await context.reply(f"Failed to retrieve resource: {results['error']}")
            return

        await process.create_artifact(
            mimetype="application/json",
            description=f"Resource details for UUID {params.uuid}",
            content=json.dumps(results, indent=2).encode('utf-8')
        )

        resource_type = results.get("type", "unknown")
        await context.reply(f"Retrieved {resource_type} resource information for UUID {params.uuid}.")
