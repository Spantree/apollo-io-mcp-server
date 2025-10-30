from mcp.server.fastmcp import FastMCP
from apollo_client import ApolloClient
from apollo import *
from typing import Optional, List

import os

from dotenv import load_dotenv
load_dotenv()
# Also load .env.secrets if present
load_dotenv('.env.secrets')

# Support both APOLLO_API_KEY and APOLLO_IO_API_KEY
api_key = os.getenv("APOLLO_API_KEY") or os.getenv("APOLLO_IO_API_KEY")
apollo_client = ApolloClient(api_key=api_key)

mcp = FastMCP("Apollo.io")

@mcp.tool()
async def people_enrichment(query: PeopleEnrichmentQuery) -> Optional[dict]:
    """
    Use the People Enrichment endpoint to enrich data for 1 person.
    https://docs.apollo.io/reference/people-enrichment
    """
    result = await apollo_client.people_enrichment(query)
    return result.model_dump() if result else None

@mcp.tool()
async def organization_enrichment(query: OrganizationEnrichmentQuery) -> Optional[dict]:
    """
    Use the Organization Enrichment endpoint to enrich data for 1 company.
    https://docs.apollo.io/reference/organization-enrichment
    """
    result = await apollo_client.organization_enrichment(query)
    return result.model_dump() if result else None

@mcp.tool()
async def people_search(query: PeopleSearchQuery) -> Optional[dict]:
    """
    Use the People Search endpoint to find people.
    https://docs.apollo.io/reference/people-search
    """
    result = await apollo_client.people_search(query)
    return result.model_dump() if result else None

@mcp.tool()
async def organization_search(query: OrganizationSearchQuery) -> Optional[dict]:
    """
    Use the Organization Search endpoint to find organizations.
    https://docs.apollo.io/reference/organization-search
    """
    result = await apollo_client.organization_search(query)
    return result.model_dump() if result else None

@mcp.tool()
async def organization_job_postings(organization_id: str) -> Optional[dict]:
    """
    Use the Organization Job Postings endpoint to find job postings for a specific organization.
    https://docs.apollo.io/reference/organization-jobs-postings
    """
    result = await apollo_client.organization_job_postings(organization_id)
    return result.model_dump() if result else None

@mcp.tool()
async def contacts_search(
    query: Optional[str] = None,
    label_ids: Optional[List[str]] = None,
    page: int = 1,
    per_page: int = 25
) -> Optional[dict]:
    """
    Search contacts saved to YOUR Apollo CRM (not global people search).

    This searches contacts you've already saved to your Apollo account,
    not the global Apollo database. Use people_search for prospecting.

    Returns contact_id which is required for contact_update operations.

    Args:
        query: Search query - matches name, email, company, title, etc.
        label_ids: Filter by list IDs (lists are called 'labels' in Apollo API)
        page: Page number (default: 1)
        per_page: Results per page (default: 25, max: 100)

    Returns:
        Dict with 'contacts' list and 'pagination' info, or None on error
    """
    result = await apollo_client.contacts_search(
        query=query,
        label_ids=label_ids,
        page=page,
        per_page=per_page
    )
    return result.model_dump() if result else None

@mcp.tool()
async def contact_create(
    first_name: str,
    last_name: str,
    email: Optional[str] = None,
    organization_name: Optional[str] = None,
    title: Optional[str] = None,
    label_names: Optional[List[str]] = None,
    phone_number: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    linkedin_url: Optional[str] = None
) -> Optional[dict]:
    """
    Create a new contact in your Apollo CRM and optionally add to lists.

    At minimum, provide first_name and last_name. Email is highly recommended
    for future contact updates and enrichment.

    Lists (label_names) will be created automatically if they don't exist.

    Returns the created contact with contact_id for future operations.

    Args:
        first_name: Contact's first name (required)
        last_name: Contact's last name (required)
        email: Email address (recommended for future updates)
        organization_name: Company/organization name
        title: Job title
        label_names: List of list names to add contact to (e.g., ["Hot Leads", "Q1 2024"])
                    Lists are called 'labels' in Apollo API but appear as 'Lists' in UI.
        phone_number: Phone number in international format (e.g., "+1-555-0123")
        city: City
        state: State/province
        country: Country code (e.g., "US")
        linkedin_url: LinkedIn profile URL

    Returns:
        Dict with created 'contact' including contact_id, or None on error
    """
    # Convert phone_number string to phone_numbers list if provided
    phone_numbers = None
    if phone_number:
        phone_numbers = [{"raw_number": phone_number, "type": "mobile"}]

    result = await apollo_client.contact_create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        organization_name=organization_name,
        title=title,
        label_names=label_names,
        phone_numbers=phone_numbers,
        city=city,
        state=state,
        country=country,
        linkedin_url=linkedin_url
    )
    return result.model_dump() if result else None

@mcp.tool()
async def contact_update(
    contact_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    organization_name: Optional[str] = None,
    title: Optional[str] = None,
    label_names: Optional[List[str]] = None,
    phone_number: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    linkedin_url: Optional[str] = None
) -> Optional[dict]:
    """
    Update an existing contact in your Apollo CRM.

    Only fields you provide will be updated. Omitted fields remain unchanged.

    IMPORTANT: label_names REPLACES the contact's lists entirely. To add to
    existing lists, first use contacts_search to get current label_names,
    then include both old and new list names.

    Use contacts_search to find the contact_id if you don't have it.

    Returns the updated contact.

    Args:
        contact_id: Contact ID from Apollo (get from contacts_search or contact_create)
        first_name: Update first name
        last_name: Update last name
        email: Update email address
        organization_name: Update company/organization name
        title: Update job title
        label_names: Update list membership - REPLACES existing lists entirely
                    (e.g., ["Hot Leads", "Q2 2024"])
                    Lists are called 'labels' in Apollo API but appear as 'Lists' in UI.
        phone_number: Update phone number (e.g., "+1-555-0123")
        city: Update city
        state: Update state/province
        country: Update country code
        linkedin_url: Update LinkedIn URL

    Returns:
        Dict with updated 'contact', or None on error
    """
    # Build fields dict with only non-None values
    fields = {}
    if first_name is not None:
        fields["first_name"] = first_name
    if last_name is not None:
        fields["last_name"] = last_name
    if email is not None:
        fields["email"] = email
    if organization_name is not None:
        fields["organization_name"] = organization_name
    if title is not None:
        fields["title"] = title
    if label_names is not None:
        fields["label_names"] = label_names
    if phone_number is not None:
        # Convert phone_number string to phone_numbers list
        fields["phone_numbers"] = [{"raw_number": phone_number, "type": "mobile"}]
    if city is not None:
        fields["city"] = city
    if state is not None:
        fields["state"] = state
    if country is not None:
        fields["country"] = country
    if linkedin_url is not None:
        fields["linkedin_url"] = linkedin_url

    result = await apollo_client.contact_update(contact_id=contact_id, **fields)
    return result.model_dump() if result else None

@mcp.tool()
async def labels_list(modality: Optional[str] = None) -> Optional[dict]:
    """
    List all labels/lists in your Apollo account.

    Labels (called "Lists" in Apollo UI) are used to organize contacts,
    accounts, and emailer campaigns. Each label has a modality field
    indicating what type of entity it contains.

    This endpoint requires a master API key. Regular API keys will fail.

    Args:
        modality: Filter by modality type. Options:
                 - "contacts": Lists of contacts/people
                 - "accounts": Lists of companies/organizations
                 - "emailer_campaigns": Lists for email campaigns
                 If None, returns all labels across all modalities.

    Returns:
        Dict with 'labels' list containing label objects (id, name, modality,
        cached_count, etc.), or None on error

    Reference:
        https://docs.apollo.io/reference/get-a-list-of-all-lists
    """
    result = await apollo_client.labels_list(modality=modality)
    return result.model_dump() if result else None

# if __name__ == "__main__":
#     mcp.run(transport="stdio")
