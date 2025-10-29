"""
Client for the OpenBiodiv API, serves as a wrapper around the OpenBiodiv REST API endpoints
"""

import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class OpenBiodivClient:
    """Client for interacting with OpenBiodiv REST API endpoints"""

    def __init__(
        self,
        api_base_url: str = "https://api.openbiodiv.net",
        api_timeout: int = 30,
        archive_timeout: int = 60
    ):
        self.api_base_url = api_base_url
        self.api_timeout = api_timeout
        self.archive_timeout = archive_timeout
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a GET request to the OpenBiodiv API with error handling

        Args:
            endpoint: API endpoint path (e.g., '/taxons')
            params: Query parameters

        Returns:
            JSON response as dictionary

        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.api_base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=self.api_timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {endpoint} - {e}")
            return {"error": str(e), "endpoint": endpoint}
        except Exception as e:
            logger.error(f"Unexpected error during API request: {endpoint} - {e}")
            return {"error": str(e), "endpoint": endpoint}

    # General Search
    def search(self, query: str) -> Dict:
        """
        General search across all resource types

        Args:
            query: Search query string

        Returns:
            Search results with id, key, type, label, and sections
        """
        return self._make_request("/search", {"q": query})

    # Taxons
    def search_taxons(self, query: str, rank: Optional[str] = None) -> Dict:
        """
        Search for taxonomic information

        Args:
            query: Scientific name or search term
            rank: Optional taxonomic rank filter

        Returns:
            Taxon results with kingdom, phylum, class, order, family, genus, species, rank, tnus
        """
        params = {"q": query}
        if rank:
            params["rank"] = rank
        return self._make_request("/taxons", params)

    def get_taxon(self, uuid: str) -> Dict:
        """
        Get detailed taxon information by UUID

        Args:
            uuid: Taxon UUID

        Returns:
            Detailed taxon information
        """
        return self._make_request(f"/taxons/{uuid}")

    # Articles
    def search_articles(self, query: str) -> Dict:
        """
        Search for biodiversity articles

        Args:
            query: Search query for articles

        Returns:
            Article results with keywords, publisher, DOI, authors
        """
        return self._make_request("/articles", {"q": query})

    def get_article(self, uuid: str) -> Dict:
        """
        Get detailed article information by UUID

        Args:
            uuid: Article UUID

        Returns:
            Detailed article information
        """
        return self._make_request(f"/articles/{uuid}")

    # Treatments
    def search_treatments(self, query: str) -> Dict:
        """
        Search for taxonomic treatments

        Args:
            query: Search query for treatments

        Returns:
            Treatment results
        """
        return self._make_request("/treatments", {"q": query})

    def get_treatment(self, uuid: str) -> Dict:
        """
        Get detailed treatment information by UUID

        Args:
            uuid: Treatment UUID

        Returns:
            Detailed treatment information
        """
        return self._make_request(f"/treatments/{uuid}")

    # Specimens
    def search_specimens(self, query: str) -> Dict:
        """
        Search for specimen records

        Args:
            query: Search query for specimens

        Returns:
            Specimen results with catalogNumber, recordedBy, sex, lifeStage,
            country, locality, typeStatus, identifiedBy, date
        """
        return self._make_request("/specimens", {"q": query})

    def get_specimen(self, uuid: str) -> Dict:
        """
        Get detailed specimen information by UUID

        Args:
            uuid: Specimen UUID

        Returns:
            Detailed specimen information
        """
        return self._make_request(f"/specimens/{uuid}")

    # Authors
    def search_authors(self, query: str) -> Dict:
        """
        Search for authors

        Args:
            query: Author name or search term

        Returns:
            Author results with articles, DOI, references, ORCID, email
        """
        return self._make_request("/authors", {"q": query})

    def get_author(self, uuid: str) -> Dict:
        """
        Get detailed author information by UUID

        Args:
            uuid: Author UUID

        Returns:
            Detailed author information
        """
        return self._make_request(f"/authors/{uuid}")

    # Institutions
    def search_institutions(self, query: str) -> Dict:
        """
        Search for institutions

        Args:
            query: Institution name or search term

        Returns:
            Institution results with mentions, articles, collection
        """
        return self._make_request("/institutions", {"q": query})

    def get_institution(self, uuid: str) -> Dict:
        """
        Get detailed institution information by UUID

        Args:
            uuid: Institution UUID

        Returns:
            Detailed institution information
        """
        return self._make_request(f"/institutions/{uuid}")

    # Sequences
    def search_sequences(self, query: str) -> Dict:
        """
        Search for genetic sequences

        Args:
            query: Search query for sequences

        Returns:
            Sequence results with mentions, collection
        """
        return self._make_request("/sequences", {"q": query})

    def get_sequence(self, uuid: str) -> Dict:
        """
        Get detailed sequence information by UUID

        Args:
            uuid: Sequence UUID

        Returns:
            Detailed sequence information
        """
        return self._make_request(f"/sequences/{uuid}")

    def get_sequences_archive(self, hash: Optional[str] = None) -> bytes:
        """
        Get sequences archive as TSV file

        Args:
            hash: Optional MD5 hash (format: Year & Week)

        Returns:
            TSV file content as bytes
        """
        endpoint = f"/sequences/archive/{hash}" if hash else "/sequences/archive"
        url = f"{self.api_base_url}{endpoint}"
        try:
            response = self.session.get(url, timeout=self.archive_timeout)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch sequences archive: {e}")
            return b""

    # Sections
    def search_sections(self, query: str) -> Dict:
        """
        Search for article sections

        Args:
            query: Search query for sections

        Returns:
            Section results with articles, collection, parent, parents, parentLabels
        """
        return self._make_request("/sections", {"q": query})

    def get_section(self, uuid: str) -> Dict:
        """
        Get detailed section information by UUID

        Args:
            uuid: Section UUID

        Returns:
            Detailed section information
        """
        return self._make_request(f"/sections/{uuid}")

    # UUIDs
    def get_by_uuid(self, uuid: str) -> Dict:
        """
        Get resource information by UUID (any resource type)

        Args:
            uuid: Resource UUID

        Returns:
            Resource information with id, uri, type, and resources array
        """
        return self._make_request(f"/uuids/{uuid}")