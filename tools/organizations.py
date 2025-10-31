"""
Organization search, enrichment, and job posting tools for Apollo.io MCP server.
"""
from typing import Optional
from apollo import OrganizationEnrichmentQuery, OrganizationSearchQuery


def register_tools(mcp, apollo_client):
    """Register all organization-related tools with the MCP server."""

    @mcp.tool()
    async def organization_enrichment(query: OrganizationEnrichmentQuery) -> Optional[dict]:
        """
        Enrich company data by domain. Returns comprehensive company info from Apollo's
        global database. Does not consume credits.

        Args:
            domain: Company domain without www (e.g., "apollo.io")

        Returns:
            Company basics, metrics, social profiles, funding, tech stack, account status

        Reference:
            https://docs.apollo.io/reference/organization-enrichment
        """
        result = await apollo_client.organization_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def organization_search(query: OrganizationSearchQuery) -> Optional[dict]:
        """
        Search 73M+ companies by size, revenue, location, technology, keywords.
        Does not consume credits. Returns organization_id for enrichment/people_search.

        Key filters: organization_num_employees_ranges, revenue_range, organization_locations,
        currently_using_any_of_technology_uids, q_organization_keyword_tags, q_organization_name

        See docs/tools/organizations.md for all filters and examples.

        Reference:
            https://docs.apollo.io/reference/organization-search
        """
        result = await apollo_client.organization_search(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def organization_job_postings(organization_id: str) -> Optional[dict]:
        """
        Get active job postings for a company. Identifies hiring signals and growth areas.
        Does not consume credits.

        Args:
            organization_id: Apollo org ID from organization_search

        Returns:
            Job postings with title, url, location, posted_at, last_seen_at

        Reference:
            https://docs.apollo.io/reference/organization-jobs-postings
        """
        result = await apollo_client.organization_job_postings(organization_id)
        return result.model_dump() if result else None
