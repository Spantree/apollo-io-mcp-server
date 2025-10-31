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
        Enrich data for a single company/organization by providing its domain name.

        This endpoint returns comprehensive information about a company from Apollo's
        global database. Does not consume credits.

        IDENTIFICATION:
        - domain: Company domain without www or @ symbol (REQUIRED)
          Examples: "apollo.io", "microsoft.com", "salesforce.com"

        RETURNED DATA:
        - Company basics (name, domain, industry, description)
        - Contact information (phone numbers, headquarters location)
        - Company metrics (employee count, revenue, founded year)
        - Social profiles (LinkedIn, Twitter, Facebook, AngelList)
        - Funding information (total funding, funding events, investors)
        - Technologies used (tech stack)
        - Account status (if saved to your CRM, label_names will show lists)

        USE CASES:
        - Research companies before outreach
        - Enrich existing company data in your CRM
        - Verify company information
        - Find company contact details

        NOTE: If the organization appears in your saved accounts, the response will
        include account field with your CRM data (owner, stage, lists).

        Reference:
            https://docs.apollo.io/reference/organization-enrichment
        """
        result = await apollo_client.organization_enrichment(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def organization_search(query: OrganizationSearchQuery) -> Optional[dict]:
        """
        Search Apollo's database of 73+ million companies to find organizations matching your criteria.

        Build targeted company lists by combining multiple filters. Does not consume credits.
        Returns organization_id which is required for organization_enrichment and people_search operations.

        SEARCH FILTERS (all optional, combine to narrow results):

        COMPANY SIZE & REVENUE:
        - organization_num_employees_ranges: Headcount ranges (e.g., ["1,10", "250,500", "10000,20000"])
        - revenue_range_min: Minimum annual revenue in dollars (e.g., 300000)
        - revenue_range_max: Maximum annual revenue in dollars (e.g., 50000000)

        LOCATION:
        - organization_locations: Company HQ locations (e.g., ["texas", "tokyo", "spain"])
        - organization_not_locations: Exclude HQ locations (e.g., ["minnesota", "ireland"])

        TECHNOLOGY & KEYWORDS:
        - currently_using_any_of_technology_uids: Technologies in use (e.g., ["salesforce", "google_analytics"])
          See full list: https://api.apollo.io/v1/auth/supported_technologies_csv
          Use underscores for spaces (e.g., "wordpress_org")
        - q_organization_keyword_tags: Industry/keyword associations (e.g., ["mining", "sales strategy"])
        - q_organization_name: Filter by company name (partial matches OK, e.g., "apollo")

        SPECIFIC TARGETS:
        - organization_ids: Apollo organization IDs (e.g., ["5e66b6381e05b4008c8331b8"])

        PAGINATION:
        - page: Page number (e.g., 1, 2, 3)
        - per_page: Results per page (default: 25, affects performance)

        RETURNED DATA:
        - Company basics (name, domain, organization_id, industry)
        - Contact information (phone, headquarters address)
        - Company metrics (employee count, revenue, founded year)
        - Social profiles (LinkedIn, Twitter, Facebook, AngelList)
        - Account status (if saved to CRM, includes label_names)

        USE CASES:
        - Build target account lists
        - Find companies by industry or size
        - Identify companies using specific technologies
        - Research companies in specific markets

        IMPORTANT: Use organization_id from results to:
        - Get full details with organization_enrichment
        - Find employees with people_search (organization_ids parameter)
        - Save to CRM with account_create

        NOTE: If organizations appear in your saved accounts, label_names will show
        which lists they're in, indicating they're already in your CRM.

        Reference:
            https://docs.apollo.io/reference/organization-search
        """
        result = await apollo_client.organization_search(query)
        return result.model_dump() if result else None

    @mcp.tool()
    async def organization_job_postings(organization_id: str) -> Optional[dict]:
        """
        Retrieve active job postings for a specific company/organization.

        Find current open positions at a company to identify hiring signals, growth areas,
        and potential decision makers. Does not consume credits.

        REQUIRED PARAMETER:
        - organization_id: Apollo organization ID (REQUIRED)
          Get this from organization_search results
          Example: "5e66b6381e05b4008c8331b8"

        RETURNED DATA (per job posting):
        - id: Job posting ID
        - title: Job title (e.g., "Senior Software Engineer")
        - url: Link to job posting
        - location: City, state, country where role is based
        - posted_at: When job was posted
        - last_seen_at: Most recent date job was seen active

        USE CASES:
        - Identify hiring signals (company growth, new departments)
        - Find relevant decision makers (hiring managers, department heads)
        - Prioritize outreach based on company needs
        - Research company structure and growth areas
        - Time outreach when companies are actively hiring

        WORKFLOW:
        1. Use organization_search to find companies
        2. Get organization_id from results
        3. Call this endpoint to see job postings
        4. Use people_search with person_titles matching job postings to find hiring managers

        Example: If company has "VP of Marketing" job posting, search for current
        employees with "CMO" or "Marketing Director" titles as potential decision makers.

        Reference:
            https://docs.apollo.io/reference/organization-jobs-postings
        """
        result = await apollo_client.organization_job_postings(organization_id)
        return result.model_dump() if result else None
