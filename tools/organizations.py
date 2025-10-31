"""
Organization search, enrichment, and job posting tools for Apollo.io MCP server.
"""
from typing import Optional
from apollo import OrganizationEnrichmentQuery, OrganizationSearchQuery


def register_tools(mcp, apollo_client):
    """Register all organization-related tools with the MCP server."""

    @mcp.tool()
    async def organization_enrichment(query: OrganizationEnrichmentQuery) -> Optional[dict]:
        """Enrich data for a single company/organization by providing its domain name.

See docs/tools/organizations.md for detailed documentation and examples.

RETURNED DATA:
        - Company basics (name, domain, industry, description)
        - Contact information (phone numbers, headquarters location)
        - Company metrics (employee count, revenue, f..."""
        result = await apollo_client.organization_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def organization_search(query: OrganizationSearchQuery) -> Optional[dict]:
        """Search Apollo's database of 73+ million companies to find organizations matching your criteria.

See docs/tools/organizations.md for detailed documentation and examples.

RETURNED DATA:
        - Company basics (name, domain, organization_id, industry)
        - Contact information (phone, headquarters address)
        - Company metrics (employee count, revenue, founde..."""
        result = await apollo_client.organization_search(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def organization_job_postings(organization_id: str) -> Optional[dict]:
        """Retrieve active job postings for a specific company/organization.

See docs/tools/organizations.md for detailed documentation and examples."""
        result = await apollo_client.organization_job_postings(organization_id)
        return result.model_dump() if result else None
