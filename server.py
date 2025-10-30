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
async def contact_search(
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
    result = await apollo_client.contact_search(
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
async def contact_bulk_create(contacts: List[dict]) -> Optional[dict]:
    """
    Bulk create up to 100 contacts in your Apollo CRM.

    This is much more efficient than creating contacts one-by-one.
    If a contact already exists (matched by email), it will be returned
    in existing_contacts array but will NOT be updated.

    Lists (label_names) will be created automatically if they don't exist.

    Args:
        contacts: List of contact dictionaries (max 100), each containing:
                 - first_name (required)
                 - last_name (required)
                 - email (optional but recommended for deduplication)
                 - organization_name, title, label_names, etc. (optional)

                 Example:
                 [
                   {
                     "first_name": "John",
                     "last_name": "Doe",
                     "email": "john@example.com",
                     "title": "CEO",
                     "organization_name": "Example Corp",
                     "label_names": ["Hot Leads"]
                   },
                   ...
                 ]

    Returns:
        Dict with:
        - 'created_contacts': Array of newly created contacts
        - 'existing_contacts': Array of contacts that already existed
        Or None on error

    Reference:
        https://docs.apollo.io/reference/create-contacts-bulk
    """
    result = await apollo_client.contact_bulk_create(contacts=contacts)
    return result.model_dump() if result else None

@mcp.tool()
async def contact_bulk_update(contacts: List[dict]) -> Optional[dict]:
    """
    Bulk update up to 100 contacts in your Apollo CRM.

    This is much more efficient than updating contacts one-by-one.
    Only provided fields will be updated for each contact.

    IMPORTANT: label_names REPLACES the contact's lists entirely for each contact.

    Args:
        contacts: List of contact dictionaries (max 100), each containing:
                 - id (required) - Apollo contact ID
                 - Any fields to update (first_name, last_name, email, title, etc.)

                 Example:
                 [
                   {
                     "id": "contact_id_1",
                     "title": "Senior CEO",
                     "label_names": ["Hot Leads", "Q1 2024"]
                   },
                   {
                     "id": "contact_id_2",
                     "email": "newemail@example.com"
                   },
                   ...
                 ]

    Returns:
        Dict with 'contacts' array of updated contacts, or None on error

    Reference:
        https://docs.apollo.io/reference/update-contacts-bulk
    """
    result = await apollo_client.contact_bulk_update(contacts=contacts)
    return result.model_dump() if result else None

@mcp.tool()
async def account_search(
    query: Optional[str] = None,
    label_ids: Optional[List[str]] = None,
    page: int = 1,
    per_page: int = 25
) -> Optional[dict]:
    """
    Search accounts saved to YOUR Apollo CRM (not global organization search).

    This searches accounts you've already saved to your Apollo account,
    not the global Apollo database. Use organization_search for prospecting.

    Returns account_id which is required for account_update operations.

    Args:
        query: Search query - matches name, domain, etc.
        label_ids: Filter by list IDs (lists are called 'labels' in Apollo API)
        page: Page number (default: 1)
        per_page: Results per page (default: 25, max: 100)

    Returns:
        Dict with 'accounts' list and 'pagination' info, or None on error

    Reference:
        https://docs.apollo.io/reference/search-for-accounts
    """
    result = await apollo_client.account_search(
        query=query,
        label_ids=label_ids,
        page=page,
        per_page=per_page
    )
    return result.model_dump() if result else None

@mcp.tool()
async def account_create(
    name: str,
    domain: Optional[str] = None,
    owner_id: Optional[str] = None,
    account_stage_id: Optional[str] = None,
    phone: Optional[str] = None,
    raw_address: Optional[str] = None,
    label_names: Optional[List[str]] = None
) -> Optional[dict]:
    """
    Create a new account in your Apollo CRM and optionally add to lists.

    IMPORTANT: This endpoint requires a master API key. Regular API keys will fail.

    At minimum, provide name. Domain is recommended for deduplication.

    Lists (label_names) will be created automatically if they don't exist.

    Returns the created account with account_id for future operations.

    Args:
        name: Account name (required, e.g., "Example Corp")
        domain: Domain name without www (e.g., "example.com")
        owner_id: Apollo user ID for account owner
        account_stage_id: Apollo ID for account stage
        phone: Primary phone number
        raw_address: Corporate location (e.g., "Dallas, United States")
        label_names: List names to add account to (e.g., ["Target Accounts", "Q1 2024"])
                    Lists are called 'labels' in Apollo API but appear as 'Lists' in UI.

    Returns:
        Dict with created 'account' including account_id, or None on error

    Reference:
        https://docs.apollo.io/reference/create-an-account
    """
    result = await apollo_client.account_create(
        name=name,
        domain=domain,
        owner_id=owner_id,
        account_stage_id=account_stage_id,
        phone=phone,
        raw_address=raw_address,
        label_names=label_names
    )
    return result.model_dump() if result else None

@mcp.tool()
async def account_update(
    account_id: str,
    name: Optional[str] = None,
    domain: Optional[str] = None,
    owner_id: Optional[str] = None,
    account_stage_id: Optional[str] = None,
    phone: Optional[str] = None,
    raw_address: Optional[str] = None,
    label_names: Optional[List[str]] = None
) -> Optional[dict]:
    """
    Update an existing account in your Apollo CRM.

    IMPORTANT: This endpoint requires a master API key. Regular API keys will fail.

    Only fields you provide will be updated. Omitted fields remain unchanged.

    IMPORTANT: label_names REPLACES the account's lists entirely. To add to
    existing lists, first use account_search to get current label_names,
    then include both old and new list names.

    Use account_search to find the account_id if you don't have it.

    Returns the updated account.

    Args:
        account_id: Account ID from Apollo (get from account_search or account_create)
        name: Update account name
        domain: Update domain
        owner_id: Update account owner
        account_stage_id: Update account stage
        phone: Update phone number
        raw_address: Update address
        label_names: Update list membership - REPLACES existing lists entirely
                    (e.g., ["Target Accounts", "Q2 2024"])
                    Lists are called 'labels' in Apollo API but appear as 'Lists' in UI.

    Returns:
        Dict with updated 'account', or None on error

    Reference:
        https://docs.apollo.io/reference/update-an-account
    """
    # Build fields dict with only non-None values
    fields = {}
    if name is not None:
        fields["name"] = name
    if domain is not None:
        fields["domain"] = domain
    if owner_id is not None:
        fields["owner_id"] = owner_id
    if account_stage_id is not None:
        fields["account_stage_id"] = account_stage_id
    if phone is not None:
        fields["phone"] = phone
    if raw_address is not None:
        fields["raw_address"] = raw_address
    if label_names is not None:
        fields["label_names"] = label_names

    result = await apollo_client.account_update(account_id=account_id, **fields)
    return result.model_dump() if result else None

@mcp.tool()
async def account_bulk_create(accounts: List[dict]) -> Optional[dict]:
    """
    Bulk create up to 100 accounts in your Apollo CRM.

    IMPORTANT: This endpoint requires a master API key. Regular API keys will fail.

    This is much more efficient than creating accounts one-by-one.
    If an account already exists (matched by domain), it will be returned
    in existing_accounts array but will NOT be updated.

    Lists (label_names) will be created automatically if they don't exist.

    Args:
        accounts: List of account dictionaries (max 100), each containing:
                 - name (required)
                 - domain (optional but recommended for deduplication)
                 - owner_id, account_stage_id, phone, raw_address, label_names (optional)

                 Example:
                 [
                   {
                     "name": "Example Corp",
                     "domain": "example.com",
                     "phone": "555-1234",
                     "raw_address": "San Francisco, CA",
                     "label_names": ["Target Accounts"]
                   },
                   ...
                 ]

    Returns:
        Dict with:
        - 'created_accounts': Array of newly created accounts
        - 'existing_accounts': Array of accounts that already existed
        Or None on error

    Reference:
        https://docs.apollo.io/reference/bulk-create-accounts
    """
    result = await apollo_client.account_bulk_create(accounts=accounts)
    return result.model_dump() if result else None

@mcp.tool()
async def account_bulk_update(accounts: List[dict]) -> Optional[dict]:
    """
    Bulk update up to 100 accounts in your Apollo CRM.

    IMPORTANT: This endpoint requires a master API key. Regular API keys will fail.

    This is much more efficient than updating accounts one-by-one.
    Only provided fields will be updated for each account.

    IMPORTANT: label_names REPLACES the account's lists entirely for each account.

    Args:
        accounts: List of account dictionaries (max 100), each containing:
                 - id (required) - Apollo account ID
                 - Any fields to update (name, domain, owner_id, etc.)

                 Example:
                 [
                   {
                     "id": "account_id_1",
                     "phone": "+1-555-5678",
                     "label_names": ["Target Accounts", "Q1 2024"]
                   },
                   {
                     "id": "account_id_2",
                     "domain": "newdomain.com"
                   },
                   ...
                 ]

    Returns:
        Dict with 'accounts' array of updated accounts, or None on error

    Reference:
        https://docs.apollo.io/reference/bulk-update-accounts
    """
    result = await apollo_client.account_bulk_update(accounts=accounts)
    return result.model_dump() if result else None

@mcp.tool()
async def usage_stats() -> Optional[dict]:
    """
    Get API usage statistics and rate limits for your Apollo account.

    Returns rate limits per endpoint showing:
    - Minute limits (limit, consumed, left_over)
    - Hour limits (limit, consumed, left_over)
    - Day limits (limit, consumed, left_over)

    This is useful for monitoring your API usage and avoiding rate limit errors.

    IMPORTANT: This endpoint requires a master API key. Regular API keys will
    receive a 403 Forbidden error.

    Returns:
        Dict with rate limit stats keyed by endpoint identifier, or None on error

    Reference:
        https://docs.apollo.io/reference/get-usage-stats
    """
    result = await apollo_client.usage_stats()
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
