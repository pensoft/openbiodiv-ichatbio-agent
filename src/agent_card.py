"""
Agent Card for the OpenBiodiv Agent.
"""

from ichatbio.types import AgentCard, AgentEntrypoint
from pydantic import BaseModel, Field
from typing import Optional


# Parameter Models
class GeneralSearchParams(BaseModel):
    """Parameters for general search across all resource types"""
    query: str = Field(description="Search query string")


class TaxonSearchParams(BaseModel):
    """Parameters for searching taxonomic information"""
    query: str = Field(description="Scientific name or search term for taxon")
    rank: Optional[str] = Field(
        default=None,
        description="Optional taxonomic rank filter (e.g., species, genus, family)"
    )


class ArticleSearchParams(BaseModel):
    """Parameters for searching biodiversity articles"""
    query: str = Field(description="Search query for articles")


class TreatmentSearchParams(BaseModel):
    """Parameters for searching taxonomic treatments"""
    query: str = Field(description="Search query for treatments")


class SpecimenSearchParams(BaseModel):
    """Parameters for searching specimen records"""
    query: str = Field(description="Search query for specimens")


class AuthorSearchParams(BaseModel):
    """Parameters for searching authors"""
    query: str = Field(description="Author name or search term")


class InstitutionSearchParams(BaseModel):
    """Parameters for searching institutions"""
    query: str = Field(description="Institution name or search term")


class SequenceSearchParams(BaseModel):
    """Parameters for searching genetic sequences"""
    query: str = Field(description="Search query for genetic sequences")


class SectionSearchParams(BaseModel):
    """Parameters for searching article sections"""
    query: str = Field(description="Search query for article sections")


class UUIDParams(BaseModel):
    """Parameters for retrieving resources by UUID"""
    uuid: str = Field(description="Resource UUID identifier")


# Agent Card Builder
def build_agent_card(url: str, icon: str) -> AgentCard:
    """
    Build the agent card with dynamic URL and icon

    Args:
        url: The public URL where the agent is accessible
        icon: The URL to the agent's icon image

    Returns:
        AgentCard with configured URL and icon
    """
    return AgentCard(
        name="OpenBiodiv Agent",
        description="An agent for querying biodiversity knowledge from the OpenBiodiv database, "
                    "including taxonomic names, treatments, specimens, sequences, scientific articles, "
                    "authors, institutions, and sections. Access comprehensive biodiversity data via REST API.",
        icon=icon,
        url=url,
        entrypoints=[
        # General Search
        AgentEntrypoint(
            id="search",
            description="Search across all resource types in OpenBiodiv database",
            parameters=GeneralSearchParams
        ),
        # Taxons
        AgentEntrypoint(
            id="search_taxons",
            description="Search for taxonomic information by scientific name with optional rank filter",
            parameters=TaxonSearchParams
        ),
        AgentEntrypoint(
            id="get_taxon",
            description="Get detailed taxon information by UUID",
            parameters=UUIDParams
        ),
        # Articles
        AgentEntrypoint(
            id="search_articles",
            description="Search for biodiversity scientific articles",
            parameters=ArticleSearchParams
        ),
        AgentEntrypoint(
            id="get_article",
            description="Get detailed article information by UUID",
            parameters=UUIDParams
        ),
        # Treatments
        AgentEntrypoint(
            id="search_treatments",
            description="Search for taxonomic treatments in scientific literature",
            parameters=TreatmentSearchParams
        ),
        AgentEntrypoint(
            id="get_treatment",
            description="Get detailed treatment information by UUID",
            parameters=UUIDParams
        ),
        # Specimens
        AgentEntrypoint(
            id="search_specimens",
            description="Get details about available resources and fetch sparql links about specific templates",
            parameters=SpecimenSearchParams
        ),
        AgentEntrypoint(
            id="get_specimen",
            description="Get detailed specimen information by UUID",
            parameters=UUIDParams
        ),
        # Authors
        AgentEntrypoint(
            id="search_authors",
            description="Search for authors and their publications",
            parameters=AuthorSearchParams
        ),
        AgentEntrypoint(
            id="get_author",
            description="Get detailed author information by UUID",
            parameters=UUIDParams
        ),
        # Institutions
        AgentEntrypoint(
            id="search_institutions",
            description="Search for institutions and their collections",
            parameters=InstitutionSearchParams
        ),
        AgentEntrypoint(
            id="get_institution",
            description="Get detailed institution information by UUID",
            parameters=UUIDParams
        ),
        # Sequences
        AgentEntrypoint(
            id="search_sequences",
            description="Search for genetic sequences",
            parameters=SequenceSearchParams
        ),
        AgentEntrypoint(
            id="get_sequence",
            description="Get detailed sequence information by UUID",
            parameters=UUIDParams
        ),
        # Sections
        AgentEntrypoint(
            id="search_sections",
            description="Search for article sections",
            parameters=SectionSearchParams
        ),
        AgentEntrypoint(
            id="get_section",
            description="Get detailed section information by UUID",
            parameters=UUIDParams
        ),
        # Generic UUID lookup
        AgentEntrypoint(
            id="get_by_uuid",
            description="Get details about available resources and fetch sparql links about specific templates",
            parameters=UUIDParams
        ),
        ]
    )