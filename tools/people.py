"""
People search and enrichment tools for Apollo.io MCP server.
"""
from typing import Optional
from apollo import PeopleEnrichmentQuery, BulkPeopleEnrichmentQuery, PeopleSearchQuery


def register_tools(mcp, apollo_client):
    """Register all people-related tools with the MCP server."""

    @mcp.tool()
    async def people_enrichment(query: PeopleEnrichmentQuery) -> Optional[dict]:
        """Enrich data for a single person by providing identifying information.

See docs/tools/people.md for detailed documentation and examples.

RETURNED DATA:
        - Person details (name, title, email, photo, social profiles)
        - Employment history (current and previous positions)
        - Organization details (employer information)..."""
        result = await apollo_client.people_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def people_bulk_enrichment(query: BulkPeopleEnrichmentQuery) -> Optional[dict]:
        """Enrich data for up to 10 people in a single request.

See docs/tools/people.md for detailed documentation and examples.

RETURNED DATA:
        - status: Operation status
        - total_requested_enrichments: Total number of enrichments requested
        - unique_enriched_records: Number successfully enriched
        -..."""
        result = await apollo_client.people_bulk_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def people_search(query: PeopleSearchQuery) -> Optional[dict]:
        """Search Apollo's database of 275+ million contacts to find people matching your criteria.

See docs/tools/people.md for detailed documentation and examples.

RETURNED DATA:
        - Person details (name, title, email, photo, person_id)
        - Employment history (current and previous positions)
        - Organization details (current employer informatio..."""
        result = await apollo_client.people_search(query)
        return result.model_dump() if result else None
