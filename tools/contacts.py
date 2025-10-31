"""
Contact CRUD operations tools for Apollo.io MCP server.
"""
from typing import Optional, List


def register_tools(mcp, apollo_client):
    """Register all contact-related tools with the MCP server."""

    @mcp.tool()
    async def contact_search(
        query: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Optional[dict]:
        """
        Search contacts saved to YOUR CRM (not global search). Returns contact_id for updates.
        Use people_search for prospecting.

        Args:
            query: Matches name, email, company, title, etc.
            label_ids: Filter by list IDs
            page: Page number (default: 1)
            per_page: Results per page (default: 25, max: 100)
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
        Create new contact in Apollo CRM and optionally add to lists.

        Provide first_name and last_name (required). Email recommended for future updates.
        Lists auto-created if they don't exist.

        Args:
            first_name: First name (required)
            last_name: Last name (required)
            email: Email (recommended)
            organization_name: Company name
            title: Job title
            label_names: List names to add contact to
            phone_number: Phone in international format
            city: City
            state: State/province
            country: Country code (e.g., "US")
            linkedin_url: LinkedIn profile URL

        Returns:
            Dict with created contact including contact_id, or None on error
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
        Update existing contact in Apollo CRM.

        Only provided fields updated. IMPORTANT: label_names REPLACES all lists.
        Get current labels from contact_search to preserve existing lists.

        Args:
            contact_id: Contact ID (from contact_search or contact_create)
            first_name: Update first name
            last_name: Update last name
            email: Update email
            organization_name: Update company name
            title: Update job title
            label_names: REPLACES existing lists entirely
            phone_number: Update phone (e.g., "+1-555-0123")
            city: Update city
            state: Update state
            country: Update country code
            linkedin_url: Update LinkedIn URL

        Returns:
            Dict with updated contact, or None on error
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
        Bulk create up to 100 contacts.

        More efficient than one-by-one creation. Existing contacts (matched by email)
        returned in existing_contacts but NOT updated.

        Args:
            contacts: List of contact dicts (max 100), each with:
                     - first_name (required)
                     - last_name (required)
                     - email (optional, recommended for deduplication)
                     - organization_name, title, label_names, etc. (optional)

        Returns:
            {created_contacts, existing_contacts} or None on error

        Reference:
            https://docs.apollo.io/reference/create-contacts-bulk
        """
        result = await apollo_client.contact_bulk_create(contacts=contacts)
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def contact_bulk_update(contacts: List[dict]) -> Optional[dict]:
        """
        Bulk update up to 100 contacts.

        More efficient than one-by-one updates. Only provided fields updated.
        IMPORTANT: label_names REPLACES all lists for each contact.

        Args:
            contacts: List of contact dicts (max 100), each with:
                     - id (required) - Apollo contact ID
                     - Any fields to update (first_name, last_name, email, title, etc.)

        Returns:
            {contacts: [updated contacts]} or None on error

        Reference:
            https://docs.apollo.io/reference/update-contacts-bulk
        """
        result = await apollo_client.contact_bulk_update(contacts=contacts)
        return result.model_dump() if result else None

    @mcp.tool()
    async def contact_add_to_list(
        contact_ids: List[str],
        label_name: str
    ) -> Optional[dict]:
        """
        Add contacts to a list without losing existing labels (max 10). Master API key required.

        Helper tool that safely merges new label with current labels. Solves label replacement
        problem - contact_update/contact_bulk_update REPLACE all labels, this tool preserves them.

        Args:
            contact_ids: Contact IDs to add (max 10)
            label_name: List name (auto-created if doesn't exist)

        Returns:
            {updated_contacts, found_ids, not_found_ids, total_requested}
        """
        result = await apollo_client.contact_add_to_list(
            contact_ids=contact_ids,
            label_name=label_name
        )
        return result
    
    @mcp.tool()
    async def contact_remove_from_list(
        contact_ids: List[str],
        label_name: str
    ) -> Optional[dict]:
        """
        Remove contacts from a list without affecting other labels (max 10). Master API key required.

        Helper tool that safely removes specified label while preserving all other labels.
        Solves label replacement problem by fetching current labels, removing target label,
        and updating with remaining labels.

        Args:
            contact_ids: Contact IDs to remove (max 10)
            label_name: List name to remove contacts from

        Returns:
            {updated_contacts, found_ids, not_found_ids, total_requested}
        """
        result = await apollo_client.contact_remove_from_list(
            contact_ids=contact_ids,
            label_name=label_name
        )
        return result
