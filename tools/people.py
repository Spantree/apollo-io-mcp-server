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
        Enrich data for a single person by providing identifying information.

        Apollo uses the information you provide to identify the correct person and return
        enriched data including employment history, contact information, and organization details.

        IDENTIFICATION PARAMETERS (provide one or more):
        - id: Apollo person ID (from people_search results, field: person_id)
        - email: Email address (e.g., "example@email.com")
        - name: Full name (e.g., "Tim Zheng") OR first_name + last_name
        - linkedin_url: LinkedIn profile URL
        - hashed_email: MD5 or SHA-256 hashed email
        - domain + (name OR first_name/last_name): Employer domain + person's name
        - organization_name + (name OR first_name/last_name): Employer name + person's name

        CREDIT CONSUMPTION:
        - reveal_personal_emails=true: May consume credits to reveal personal emails
        - reveal_phone_number=true: May consume credits to reveal phone numbers
        - Basic enrichment: Does not consume credits

        PHONE NUMBER REVEAL:
        - If reveal_phone_number=true, webhook_url is REQUIRED
        - Phone numbers are delivered asynchronously to your webhook (may take several minutes)
        - The webhook receives a separate JSON response with phone number details

        GDPR COMPLIANCE:
        - Personal emails will NOT be revealed for people in GDPR-compliant regions

        RETURNED DATA:
        - Person details (name, title, email, photo, social profiles)
        - Employment history (current and previous positions)
        - Organization details (employer information)
        - Contact information (email status, phone numbers if requested)
        - Engagement signals (is_likely_to_engage, intent_strength)
        - Professional details (departments, seniority, functions)

        https://docs.apollo.io/reference/people-enrichment
        """
        result = await apollo_client.people_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def people_bulk_enrichment(query: BulkPeopleEnrichmentQuery) -> Optional[dict]:
        """
        Enrich data for up to 10 people in a single request.

        This endpoint is more efficient than multiple individual enrichment calls.
        Provide an array of person identification objects (up to 10 people).

        IDENTIFICATION PARAMETERS (for each person in details array):
        - id: Apollo person ID
        - email: Email address
        - name: Full name OR first_name + last_name
        - linkedin_url: LinkedIn profile URL
        - hashed_email: MD5 or SHA-256 hashed email
        - domain + (name OR first_name/last_name): Employer domain + person's name
        - organization_name + (name OR first_name/last_name): Employer name + person's name

        CREDIT CONSUMPTION:
        - reveal_personal_emails=true: May consume credits to reveal personal emails for ALL matched people
        - reveal_phone_number=true: May consume credits to reveal phone numbers for ALL matched people
        - Basic enrichment: Does not consume credits

        PHONE NUMBER REVEAL:
        - If reveal_phone_number=true, webhook_url is REQUIRED
        - Phone numbers are delivered asynchronously to your webhook (may take several minutes)
        - The webhook receives a separate JSON response with phone number details

        GDPR COMPLIANCE:
        - Personal emails will NOT be revealed for people in GDPR-compliant regions

        RETURNED DATA:
        - status: Operation status
        - total_requested_enrichments: Total number of enrichments requested
        - unique_enriched_records: Number successfully enriched
        - missing_records: Number of records not found
        - credits_consumed: Credits used by this operation
        - matches: Array of enriched Person objects (same structure as people_enrichment)

        Example request:
        {
          "details": [
            {"email": "person1@example.com"},
            {"id": "6017beeb93f2c70001751d3c"},
            {"name": "John Doe", "domain": "example.com"}
          ],
          "reveal_personal_emails": false
        }

        https://docs.apollo.io/reference/bulk-people-enrichment
        """
        result = await apollo_client.people_bulk_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def people_search(query: PeopleSearchQuery) -> Optional[dict]:
        """
        Search Apollo's database of 275+ million contacts to find people matching your criteria.

        Build targeted prospect lists by combining multiple filters. Does not consume credits.
        Returns person_id which is required for people_enrichment operations.

        SEARCH FILTERS (all optional, combine to narrow results):

        PERSON ATTRIBUTES:
        - person_titles: Job titles (e.g., ["marketing manager", "sales director"])
          Matches similar titles unless include_similar_titles=false
        - person_seniorities: Seniority levels (e.g., ["c_suite", "vp", "director"])
          Options: owner, founder, c_suite, partner, vp, head, director, manager, senior, entry, intern
        - person_locations: Where people live (e.g., ["california", "ireland", "chicago"])
        - contact_email_status: Email quality (e.g., ["verified", "likely to engage"])
          Options: verified, unverified, likely to engage, unavailable

        COMPANY FILTERS:
        - organization_ids: Apollo organization IDs from organization_search (e.g., ["5e66b6381e05b4008c8331b8"])
        - q_organization_domains_list: Employer domains (up to 1000, e.g., ["apollo.io", "microsoft.com"])
        - organization_locations: Company HQ location (e.g., ["texas", "tokyo", "spain"])
        - organization_num_employees_ranges: Company size (e.g., ["1,10", "250,500", "10000,20000"])

        OTHER FILTERS:
        - q_keywords: Keyword search across profile data

        PAGINATION:
        - page: Page number (e.g., 1, 2, 3)
        - per_page: Results per page (default: 25, affects performance)

        RETURNED DATA:
        - Person details (name, title, email, photo, person_id)
        - Employment history (current and previous positions)
        - Organization details (current employer information)
        - Contact information (email status, phone numbers)
        - Professional metadata (departments, seniority, functions)

        USE CASES:
        - Build targeted prospect lists
        - Find decision makers at specific companies
        - Identify people by job function and seniority
        - Research contacts before outreach

        IMPORTANT: Use person_id from results with people_enrichment endpoint for full details.
        To save contacts to your CRM, use contact_create or contact_bulk_create.

        Reference:
            https://docs.apollo.io/reference/people-search
        """
        result = await apollo_client.people_search(query)
        return result.model_dump() if result else None
