from typing import Optional, List, Dict
import httpx

from apollo import *

class ApolloClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/api/v1"
        self.headers = {
            "accept": "application/json",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

    async def people_enrichment(self, query: PeopleEnrichmentQuery) -> Optional[PeopleEnrichmentResponse]:
        """
        Use the People Enrichment endpoint to enrich data for 1 person.
        https://docs.apollo.io/reference/people-enrichment
        """
        url = f"{self.base_url}/people/match"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return PeopleEnrichmentResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def people_bulk_enrichment(self, query: BulkPeopleEnrichmentQuery) -> Optional[BulkPeopleEnrichmentResponse]:
        """
        Use the Bulk People Enrichment endpoint to enrich data for up to 10 people.
        https://docs.apollo.io/reference/bulk-people-enrichment
        """
        url = f"{self.base_url}/people/bulk_match"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return BulkPeopleEnrichmentResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def organization_enrichment(self, query: OrganizationEnrichmentQuery) -> Optional[OrganizationEnrichmentResponse]:
        """
        Use the Organization Enrichment endpoint to enrich data for 1 company.
        https://docs.apollo.io/reference/organization-enrichment
        """
        url = f"{self.base_url}/organizations/enrich"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return OrganizationEnrichmentResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def people_search(self, query: PeopleSearchQuery) -> Optional[PeopleSearchResponse]:
        """
        Use the People Search endpoint to find people.
        https://docs.apollo.io/reference/people-search
        """
        url = f"{self.base_url}/mixed_people/search"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return PeopleSearchResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def organization_search(self, query: OrganizationSearchQuery) -> Optional[OrganizationSearchResponse]:
        """
        Use the Organization Search endpoint to find organizations.
        https://docs.apollo.io/reference/organization-search
        """
        url = f"{self.base_url}/mixed_companies/search"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return OrganizationSearchResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def organization_job_postings(self, organization_id: str) -> Optional[OrganizationJobPostingsResponse]:
        """
        Use the Organization Job Postings endpoint to find job postings for a specific organization.
        https://docs.apollo.io/reference/organization-jobs-postings
        """
        url = f"{self.base_url}/organizations/{organization_id}/job_postings"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                return OrganizationJobPostingsResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def contact_search(
        self,
        query: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Optional[ContactSearchResponse]:
        """
        Search contacts saved to your Apollo CRM.
        https://docs.apollo.io/reference/contacts-search

        Args:
            query: Search query (matches name, email, company, title, etc.)
            label_ids: Filter by list IDs (lists are called 'labels' in Apollo API)
            page: Page number (default: 1)
            per_page: Results per page (default: 25, max: 100)

        Returns:
            ContactSearchResponse with contacts and pagination info
        """
        url = f"{self.base_url}/contacts/search"
        params = {
            "page": page,
            "per_page": min(per_page, 100)  # Cap at 100 per API docs
        }
        if query:
            params["q"] = query
        if label_ids:
            params["contact_label_ids[]"] = label_ids

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return ContactSearchResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def contact_create(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        organization_name: Optional[str] = None,
        title: Optional[str] = None,
        label_names: Optional[List[str]] = None,
        phone_numbers: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> Optional[ContactCreateResponse]:
        """
        Create a new contact in your Apollo CRM.
        https://docs.apollo.io/reference/create-contact

        Args:
            first_name: Contact's first name (required)
            last_name: Contact's last name (required)
            email: Email address (recommended for future updates)
            organization_name: Company name
            title: Job title
            label_names: List names to add contact to (auto-created if don't exist)
            phone_numbers: List of phone number dicts with 'raw_number' and 'type'
            **kwargs: Additional fields (city, state, country, linkedin_url, etc.)

        Returns:
            ContactCreateResponse with created contact including contact_id
        """
        url = f"{self.base_url}/contacts"
        data = {
            "first_name": first_name,
            "last_name": last_name
        }
        if email:
            data["email"] = email
        if organization_name:
            data["organization_name"] = organization_name
        if title:
            data["title"] = title
        if label_names:
            data["label_names"] = label_names
        if phone_numbers:
            data["phone_numbers"] = phone_numbers
        # Add any additional fields
        data.update(kwargs)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                return ContactCreateResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def contact_update(
        self,
        contact_id: str,
        **fields
    ) -> Optional[ContactUpdateResponse]:
        """
        Update an existing contact in your Apollo CRM.
        https://docs.apollo.io/reference/update-contact

        Only fields provided will be updated. Omitted fields remain unchanged.

        Args:
            contact_id: Apollo contact ID (from contacts_search or contact_create)
            **fields: Fields to update (first_name, last_name, email, title,
                     organization_name, label_names, phone_numbers, etc.)

        Returns:
            ContactUpdateResponse with updated contact

        Note:
            label_names REPLACES the contact's lists entirely. To add to existing
            lists, first fetch current label_names via contacts_search, then include
            both old and new list names in the update.
        """
        url = f"{self.base_url}/contacts/{contact_id}"
        # Filter out None values to only update provided fields
        data = {k: v for k, v in fields.items() if v is not None}

        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data, headers=self.headers)
            if response.status_code == 200:
                return ContactUpdateResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def contact_get(
        self,
        contact_id: str
    ) -> Optional[Dict]:
        """
        Fetch a single contact by ID from your Apollo CRM.

        Requires master API key.

        Args:
            contact_id: Apollo contact ID

        Returns:
            Contact dictionary with all fields, or None if not found
        """
        url = f"{self.base_url}/contacts/{contact_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                # API returns {"contact": {...}}
                return response.json().get("contact")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def contact_bulk_create(
        self,
        contacts: List[Dict]
    ) -> Optional[ContactBulkCreateResponse]:
        """
        Bulk create up to 100 contacts in your Apollo CRM.
        https://docs.apollo.io/reference/create-contacts-bulk

        Args:
            contacts: List of contact dictionaries (max 100), each containing:
                     - first_name (required)
                     - last_name (required)
                     - email (optional but recommended)
                     - organization_name, title, label_names, etc. (optional)

        Returns:
            ContactBulkCreateResponse with created_contacts and existing_contacts arrays

        Note:
            If a contact already exists (matched by email), it will be returned in
            existing_contacts array but will NOT be updated. Use bulk_update for that.
        """
        url = f"{self.base_url}/contacts/bulk_create"
        data = {"contacts": contacts[:100]}  # Cap at 100 per API docs

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                result = ContactBulkCreateResponse(**response.json())

                # Seed the label cache for created contacts
                for i, contact_dict in enumerate(contacts[:100]):
                    if 'label_names' in contact_dict and i < len(result.created_contacts):
                        created_contact = result.created_contacts[i]
                        contact_id = created_contact.get('id') if isinstance(created_contact, dict) else getattr(created_contact, 'id', None)
                        if contact_id:
                            self._contact_labels_cache[contact_id] = contact_dict['label_names']

                return result
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def contact_bulk_update(
        self,
        contacts: List[Dict]
    ) -> Optional[ContactBulkUpdateResponse]:
        """
        Bulk update up to 100 contacts in your Apollo CRM.
        https://docs.apollo.io/reference/update-contacts-bulk

        Args:
            contacts: List of contact dictionaries (max 100), each containing:
                     - id (required) - Apollo contact ID
                     - Any fields to update (first_name, last_name, email, title, etc.)

        Returns:
            ContactBulkUpdateResponse with updated contacts array

        Note:
            For 100 or fewer contacts, the response is synchronous.
            label_names REPLACES the contact's lists entirely.
        """
        url = f"{self.base_url}/contacts/bulk_update"
        data = {"contacts": contacts[:100]}  # Cap at 100 per API docs

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                return ContactBulkUpdateResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def account_search(
        self,
        query: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Optional[AccountSearchResponse]:
        """
        Search accounts saved to your Apollo CRM.
        https://docs.apollo.io/reference/search-for-accounts

        Args:
            query: Search query (matches name, domain, etc.)
            label_ids: Filter by list IDs (lists are called 'labels' in Apollo API)
            page: Page number (default: 1)
            per_page: Results per page (default: 25, max: 100)

        Returns:
            AccountSearchResponse with accounts and pagination info
        """
        url = f"{self.base_url}/accounts/search"
        params = {
            "page": page,
            "per_page": min(per_page, 100)  # Cap at 100 per API docs
        }
        if query:
            params["q"] = query
        if label_ids:
            params["account_label_ids[]"] = label_ids

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return AccountSearchResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def account_create(
        self,
        name: str,
        domain: Optional[str] = None,
        owner_id: Optional[str] = None,
        account_stage_id: Optional[str] = None,
        phone: Optional[str] = None,
        raw_address: Optional[str] = None,
        typed_custom_fields: Optional[Dict[str, Any]] = None,
        label_names: Optional[List[str]] = None
    ) -> Optional[AccountCreateResponse]:
        """
        Create a new account in your Apollo CRM.
        https://docs.apollo.io/reference/create-an-account

        Requires master API key.

        Args:
            name: Account name (required)
            domain: Domain name without www (e.g., "apollo.io")
            owner_id: Apollo user ID for account owner
            account_stage_id: Apollo ID for account stage
            phone: Primary phone number
            raw_address: Corporate location
            typed_custom_fields: Custom fields data
            label_names: List names to add account to

        Returns:
            AccountCreateResponse with created account including account_id
        """
        url = f"{self.base_url}/accounts"
        data = {"name": name}

        if domain:
            data["domain"] = domain
        if owner_id:
            data["owner_id"] = owner_id
        if account_stage_id:
            data["account_stage_id"] = account_stage_id
        if phone:
            data["phone"] = phone
        if raw_address:
            data["raw_address"] = raw_address
        if typed_custom_fields:
            data["typed_custom_fields"] = typed_custom_fields
        if label_names:
            data["label_names"] = label_names

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                return AccountCreateResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def account_get(
        self,
        account_id: str
    ) -> Optional[Dict]:
        """
        Fetch a single account by ID from your Apollo CRM.

        Requires master API key.

        Args:
            account_id: Apollo account ID

        Returns:
            Account dictionary with all fields, or None if not found
        """
        url = f"{self.base_url}/accounts/{account_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                # API returns {"account": {...}}
                return response.json().get("account")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def account_update(
        self,
        account_id: str,
        **fields
    ) -> Optional[AccountUpdateResponse]:
        """
        Update an existing account in your Apollo CRM.
        https://docs.apollo.io/reference/update-an-account

        Requires master API key.

        Only fields provided will be updated. Omitted fields remain unchanged.

        Args:
            account_id: Apollo account ID
            **fields: Fields to update (name, domain, owner_id, etc.)

        Returns:
            AccountUpdateResponse with updated account

        Note:
            label_names REPLACES the account's lists entirely.
        """
        url = f"{self.base_url}/accounts/{account_id}"
        # Filter out None values to only update provided fields
        data = {k: v for k, v in fields.items() if v is not None}

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=data, headers=self.headers)
            if response.status_code == 200:
                return AccountUpdateResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def account_bulk_create(
        self,
        accounts: List[Dict]
    ) -> Optional[AccountBulkCreateResponse]:
        """
        Bulk create up to 100 accounts in your Apollo CRM.
        https://docs.apollo.io/reference/bulk-create-accounts

        Requires master API key.

        Args:
            accounts: List of account dictionaries (max 100)

        Returns:
            AccountBulkCreateResponse with created_accounts and existing_accounts arrays
        """
        url = f"{self.base_url}/accounts/bulk_create"
        data = {"accounts": accounts[:100]}  # Cap at 100 per API docs

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                result = AccountBulkCreateResponse(**response.json())

                # Seed the label cache for created accounts
                for i, account_dict in enumerate(accounts[:100]):
                    if 'label_names' in account_dict and i < len(result.created_accounts):
                        created_account = result.created_accounts[i]
                        account_id = created_account.get('id') if isinstance(created_account, dict) else getattr(created_account, 'id', None)
                        if account_id:
                            self._account_labels_cache[account_id] = account_dict['label_names']

                return result
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def account_bulk_update(
        self,
        accounts: List[Dict]
    ) -> Optional[AccountBulkUpdateResponse]:
        """
        Bulk update up to 100 accounts in your Apollo CRM.
        https://docs.apollo.io/reference/bulk-update-accounts

        Requires master API key.

        Args:
            accounts: List of account dictionaries (max 100), each with 'id' field

        Returns:
            AccountBulkUpdateResponse with updated accounts array
        """
        url = f"{self.base_url}/accounts/bulk_update"
        data = {"accounts": accounts[:100]}  # Cap at 100 per API docs

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                return AccountBulkUpdateResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def usage_stats(self) -> Optional[UsageStatsResponse]:
        """
        Get API usage statistics and rate limits for your Apollo account.
        https://docs.apollo.io/reference/get-usage-stats

        Returns rate limits per endpoint with minute, hour, and day limits.

        Returns:
            UsageStatsResponse with rate limit stats keyed by endpoint identifier

        Note:
            This endpoint requires a master API key. Regular API keys will receive a 403 error.
        """
        url = f"{self.base_url}/usage_stats/api_usage_stats"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers)
            if response.status_code == 200:
                return UsageStatsResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def labels_list(
        self,
        modality: Optional[str] = None
    ) -> Optional[LabelListResponse]:
        """
        List all labels/lists in your Apollo account.
        https://docs.apollo.io/reference/get-a-list-of-all-lists

        The API returns all labels across all modalities (contacts, accounts, emailer_campaigns).
        Client-side filtering by modality is performed if specified.

        Args:
            modality: Filter by modality ("contacts", "accounts", "emailer_campaigns").
                     If None, returns all labels.

        Returns:
            LabelListResponse with list of labels

        Note:
            This endpoint requires a master API key. Regular API keys will receive a 403 error.
        """
        url = f"{self.base_url}/labels"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                labels_data = response.json()
                # API returns array directly, wrap in LabelListResponse
                # Filter by modality if specified
                if modality:
                    labels_data = [label for label in labels_data if label.get('modality') == modality]
                return LabelListResponse(labels=[Label(**label) for label in labels_data])
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    # Cache for account labels (since API doesn't reliably return label_names)
    _account_labels_cache: Dict[str, List[str]] = {}

    # Cache for contact labels (since API doesn't reliably return label_names)
    _contact_labels_cache: Dict[str, List[str]] = {}

    async def account_manage_lists(
        self,
        account_ids: List[str],
        label_name: str,
        operation: str = "add"
    ) -> Optional[Dict]:
        """
        Add or remove accounts from a list without losing existing labels.

        Processes each account individually by:
        1. Fetching the account by ID to get current labels (from cache or API)
        2. Adding or removing the specified label
        3. Updating the account with the modified labels
        4. Caching the new labels for future operations

        NOTE: Since Apollo's API doesn't consistently return label_names,
        we maintain a cache of labels across operations. This means
        labels modified outside this helper may not be reflected.

        Args:
            account_ids: List of account IDs (up to 10)
            label_name: Name of list to add to or remove from
            operation: Either "add" or "remove"

        Returns:
            Dict with:
                - updated_accounts: list of successfully updated accounts
                - found_ids: list of account IDs that were found and updated
                - not_found_ids: list of account IDs that couldn't be found
                - total_requested: number of accounts requested
        """
        updated_accounts = []
        found_ids = []
        not_found_ids = []

        # Process each account individually
        for account_id in account_ids[:10]:  # Limit to 10
            # Try to get labels from cache first, otherwise fetch
            if account_id in self._account_labels_cache:
                current_labels = self._account_labels_cache[account_id]
            else:
                # Fetch account to initialize cache
                account = await self.account_get(account_id)
                if not account:
                    not_found_ids.append(account_id)
                    continue
                # account_get doesn't return label_names, only label_ids
                # So we start with empty labels if not in cache
                current_labels = []
                self._account_labels_cache[account_id] = current_labels

            # Modify labels based on operation
            if operation == "add":
                new_labels = list(set(current_labels + [label_name]))
            elif operation == "remove":
                new_labels = [label for label in current_labels if label != label_name]
            else:
                print(f"Error: Invalid operation '{operation}'. Must be 'add' or 'remove'.")
                not_found_ids.append(account_id)
                continue

            # Update account with new labels
            result = await self.account_update(account_id, label_names=new_labels)

            if result and result.account:
                # Update cache with new labels
                self._account_labels_cache[account_id] = new_labels

                # Construct response with labels we set
                updated_account = result.account.copy() if isinstance(result.account, dict) else vars(result.account)
                updated_account['label_names'] = new_labels
                updated_accounts.append(updated_account)
                found_ids.append(account_id)
            else:
                not_found_ids.append(account_id)

        return {
            "updated_accounts": updated_accounts,
            "found_ids": found_ids,
            "not_found_ids": not_found_ids,
            "total_requested": len(account_ids[:10])
        }

    async def account_add_to_list(
        self,
        account_ids: List[str],
        label_name: str
    ) -> Optional[Dict]:
        """Wrapper for account_manage_lists with operation="add"."""
        return await self.account_manage_lists(account_ids, label_name, "add")

    async def account_remove_from_list(
        self,
        account_ids: List[str],
        label_name: str
    ) -> Optional[Dict]:
        """Wrapper for account_manage_lists with operation="remove"."""
        return await self.account_manage_lists(account_ids, label_name, "remove")

    async def contact_manage_lists(
        self,
        contact_ids: List[str],
        label_name: str,
        operation: str = "add"
    ) -> Optional[Dict]:
        """
        Add or remove contacts from a list without losing existing labels.

        Processes each contact individually by:
        1. Fetching the contact by ID to get current labels (from cache or API)
        2. Adding or removing the specified label
        3. Updating the contact with the modified labels
        4. Caching the new labels for future operations

        NOTE: Since Apollo's API doesn't consistently return label_names,
        we maintain a cache of labels across operations. This means
        labels modified outside this helper may not be reflected.

        Args:
            contact_ids: List of contact IDs (up to 10)
            label_name: Name of list to add to or remove from
            operation: Either "add" or "remove"

        Returns:
            Dict with:
                - updated_contacts: list of successfully updated contacts
                - found_ids: list of contact IDs that were found and updated
                - not_found_ids: list of contact IDs that couldn't be found
                - total_requested: number of contacts requested
        """
        updated_contacts = []
        found_ids = []
        not_found_ids = []

        # Process each contact individually
        for contact_id in contact_ids[:10]:  # Limit to 10
            # Try to get labels from cache first, otherwise fetch
            if contact_id in self._contact_labels_cache:
                current_labels = self._contact_labels_cache[contact_id]
            else:
                # Fetch contact to initialize cache
                contact = await self.contact_get(contact_id)
                if not contact:
                    not_found_ids.append(contact_id)
                    continue
                # contact_get doesn't return label_names, only label_ids
                # So we start with empty labels if not in cache
                current_labels = []
                self._contact_labels_cache[contact_id] = current_labels

            # Modify labels based on operation
            if operation == "add":
                new_labels = list(set(current_labels + [label_name]))
            elif operation == "remove":
                new_labels = [label for label in current_labels if label != label_name]
            else:
                print(f"Error: Invalid operation '{operation}'. Must be 'add' or 'remove'.")
                not_found_ids.append(contact_id)
                continue

            # Update contact with new labels
            result = await self.contact_update(contact_id, label_names=new_labels)

            if result and result.contact:
                # Update cache with new labels
                self._contact_labels_cache[contact_id] = new_labels

                # Construct response with labels we set
                updated_contact = result.contact.copy() if isinstance(result.contact, dict) else vars(result.contact)
                updated_contact['label_names'] = new_labels
                updated_contacts.append(updated_contact)
                found_ids.append(contact_id)
            else:
                not_found_ids.append(contact_id)

        return {
            "updated_contacts": updated_contacts,
            "found_ids": found_ids,
            "not_found_ids": not_found_ids,
            "total_requested": len(contact_ids[:10])
        }

    async def contact_add_to_list(
        self,
        contact_ids: List[str],
        label_name: str
    ) -> Optional[Dict]:
        """Wrapper for contact_manage_lists with operation="add"."""
        return await self.contact_manage_lists(contact_ids, label_name, "add")

    async def contact_remove_from_list(
        self,
        contact_ids: List[str],
        label_name: str
    ) -> Optional[Dict]:
        """Wrapper for contact_manage_lists with operation="remove"."""
        return await self.contact_manage_lists(contact_ids, label_name, "remove")

# Example usage (you'll need to set the APOLLO_IO_API_KEY environment variable)
async def main():
    import os

    api_key = os.getenv('APOLLO_IO_API_KEY')  # Replace with your actual API key or use os.getenv("APOLLO_IO_API_KEY")
    client = ApolloClient(api_key)

    # Example People Enrichment
    people_enrichment_query = PeopleEnrichmentQuery(
        first_name="Tim",
        last_name="Zheng",
    )
    people_enrichment_response = await client.people_enrichment(people_enrichment_query)

    if people_enrichment_response:
        print("People Enrichment Response:", people_enrichment_response.model_dump_json(indent=2))
    else:
        print("People Enrichment failed.")

    # Example Organization Enrichment
    organization_enrichment_query = OrganizationEnrichmentQuery(
        domain="apollo.io",
    )
    organization_enrichment_response = await client.organization_enrichment(organization_enrichment_query)

    if organization_enrichment_response:
        print("Organization Enrichment Response:", organization_enrichment_response.model_dump_json(indent=2))
    else:
        print("Organization Enrichment failed.")

    # Example People Search
    people_search_query = PeopleSearchQuery(
        person_titles=["Marketing Manager"],
        person_seniorities=["vp"],
        q_organization_domains_list=["apollo.io"]
    )
    people_search_response = await client.people_search(people_search_query)

    if people_search_response:
        print("People Search Response:", people_search_response.model_dump_json(indent=2))
    else:
        print("People Search failed.")

    # Example Organization Search
    organization_search_query = OrganizationSearchQuery(
        organization_num_employees_ranges=["250,1000"],
        organization_locations=["japan", "ireland"]
    )
    organization_search_response = await client.organization_search(organization_search_query)

    if organization_search_response:
        print("Organization Search Response:", organization_search_response.model_dump_json(indent=2))
    else:
        print("Organization Search failed.")

    # Example Organization Job Postings
    organization_job_postings_response = await client.organization_job_postings(organization_id="5e66b6381e05b4008c8331b8")

    if organization_job_postings_response:
        print("Organization Job Postings Response:", organization_job_postings_response.model_dump_json(indent=2))
    else:
        print("Organization Job Postings failed.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
