"""
People search and enrichment tools for Apollo.io MCP server.
"""
from typing import Optional
from apollo import PeopleEnrichmentQuery, BulkPeopleEnrichmentQuery, PeopleSearchQuery


def register_tools(mcp, apollo_client):
    """Register all people-related tools with the MCP server."""

    @mcp.tool()
    async def people_enrichment(query: PeopleEnrichmentQuery) -> Optional[dict]:
        """
        Enrich person data by email, LinkedIn URL, name, or person_id.
        Returns employment history, contact info, and engagement signals.

        Identify by: id, email, name/first_name+last_name, linkedin_url, domain+name, or organization_name+name

        Credit usage: reveal_personal_emails or reveal_phone_number may consume credits.
        Basic enrichment is free. See docs/tools/people.md for details.

        https://docs.apollo.io/reference/people-enrichment
        """
        result = await apollo_client.people_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def people_bulk_enrichment(query: BulkPeopleEnrichmentQuery) -> Optional[dict]:
        """
        Enrich up to 10 people in one request. More efficient than individual calls.

        Provide array of person identification objects (id, email, name, linkedin_url, etc).
        Credit usage: reveal_personal_emails/reveal_phone_number may consume credits.

        Returns: {status, total_requested_enrichments, unique_enriched_records,
        missing_records, credits_consumed, matches}

        https://docs.apollo.io/reference/bulk-people-enrichment
        """
        result = await apollo_client.people_bulk_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def people_search(query: PeopleSearchQuery) -> Optional[dict]:
        """
        Search 275M+ people by title, seniority, location, company, and more.
        Does not consume credits. Returns person_id for enrichment.

        Key filters: person_titles, person_seniorities, person_locations, contact_email_status,
        organization_ids, q_organization_domains_list, organization_locations

        See docs/tools/people.md for all filters and examples.

        Reference:
            https://docs.apollo.io/reference/people-search
        """
        result = await apollo_client.people_search(query)
        return result.model_dump() if result else None
