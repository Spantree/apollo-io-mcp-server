# Apollo.io MCP Server

This project provides an MCP server that exposes the Apollo.io API functionalities as tools. It allows you to interact with the Apollo.io API using the Model Context Protocol (MCP).

## Overview

The project consists of the following main components:

- `apollo_client.py`: Defines the `ApolloClient` class, which is used to interact with the Apollo.io API. It includes methods for people enrichment, organization enrichment, people search, organization search, organization job postings, contact management, and account management.
- `server.py`: Main entry point that initializes the FastMCP server and registers all tools.
- `tools/`: Modular tool organization with focused modules for each entity type:
  - `people.py`: People search and enrichment tools
  - `organizations.py`: Organization search, enrichment, and job posting tools
  - `contacts.py`: Contact CRUD operations
  - `accounts.py`: Account CRUD and list management tools
  - `misc.py`: Usage stats and labels tools
- `apollo/`: Contains the data models for the Apollo.io API, such as `PeopleEnrichmentQuery`, `OrganizationEnrichmentQuery`, `PeopleSearchQuery`, `OrganizationSearchQuery`, contact models, account models, and more.

## Available Tools

The following 20 tools are exposed via MCP:

### People Tools (3 tools)

-   **`people_enrichment`**: Enrich data for a single person by email, LinkedIn URL, or name. Returns employment history, contact info, and engagement signals.
-   **`people_bulk_enrichment`**: Enrich up to 10 people in a single request. More efficient than multiple individual calls.
-   **`people_search`**: Search Apollo's database of 275M+ people. Filter by title, seniority, location, company, and more. Returns `person_id` for enrichment.

### Organization Tools (3 tools)

-   **`organization_enrichment`**: Enrich data for a company by domain. Returns company info, funding, tech stack, and social profiles.
-   **`organization_search`**: Search Apollo's database of 73M+ companies. Filter by size, revenue, location, technology, and industry.
-   **`organization_job_postings`**: Get active job postings for a specific organization. Useful for identifying hiring signals and decision makers.

### Contact Management Tools (5 tools)

-   **`contact_search`**: Search contacts saved to YOUR Apollo CRM (not global search). Returns `contact_id` needed for updates.
-   **`contact_create`**: Create a new contact in your Apollo CRM with optional list assignment.
-   **`contact_update`**: Update an existing contact in your Apollo CRM, including managing list membership.
-   **`contact_bulk_create`**: Bulk create up to 100 contacts in a single API call. Returns separate arrays for created and existing contacts.
-   **`contact_bulk_update`**: Bulk update up to 100 contacts in a single API call. Much more efficient than individual updates.

### Account Management Tools (7 tools)

-   **`account_search`**: Search accounts (companies) saved to YOUR Apollo CRM. Returns `account_id` needed for updates.
-   **`account_create`**: Create a new account in your Apollo CRM. **Requires master API key.**
-   **`account_update`**: Update an existing account in your Apollo CRM. **Requires master API key.**
-   **`account_bulk_create`**: Bulk create accounts in a single API call. **Requires master API key.**
-   **`account_bulk_update`**: Bulk update accounts in a single API call. **Requires master API key.**
-   **`account_add_to_list`**: Add accounts to a list WITHOUT losing their existing labels (helper tool that safely merges labels). **Requires master API key.**
-   **`account_remove_from_list`**: Remove accounts from a list while preserving other labels (helper tool for selective removal). **Requires master API key.**

### Utility Tools (2 tools)

-   **`labels_list`**: List all labels/lists in your Apollo account, with optional filtering by modality (contacts, accounts, emailer_campaigns). **Requires master API key.**
-   **`usage_stats`**: Get API usage statistics and rate limits per endpoint. **Requires master API key.**

**Note on Lists vs Labels**: Apollo's API uses the term "labels" (via `label_names` parameter), but these appear as "Lists" in the Apollo UI. They are the same thing. Lists can be automatically created when you assign contacts/accounts to them.

**Note on Master API Key**: Account write operations (create/update) and certain utility endpoints require a master API key. Contact your Apollo.io account manager to obtain one.

## Usage

To use this MCP server, you need to:

1. Set the `APOLLO_IO_API_KEY` environment variable with your Apollo.io API key. Or create '.env' file in the project root with `APOLLO_IO_API_KEY`.
2. Get dependencies: `uv sync`
3. Run the `uv run mcp run server.py`

### Usage Examples

#### Search Contacts
Search contacts you've saved to your Apollo CRM:
```python
contact_search(
    query="john@example.com",  # Search by email, name, company, etc.
    page=1,
    per_page=25
)
```

#### Create Contact
Create a new contact and add to lists:
```python
contact_create(
    first_name="Jane",
    last_name="Smith",
    email="jane@example.com",
    organization_name="Example Inc",
    title="VP of Sales",
    label_names=["Hot Leads", "Q1 2024"]  # Lists auto-created if they don't exist
)
```

#### Update Contact
Update an existing contact's information:
```python
contact_update(
    contact_id="5f7b1b5b4c9d6c0001234567",  # From contact_search or contact_create
    title="Senior VP of Sales",
    label_names=["Hot Leads", "Q2 2024"]  # REPLACES all existing lists
)
```

**Important**: `label_names` in `contact_update` REPLACES all lists. To add to existing lists:
1. Use `contact_search` to get current `label_names`
2. Merge with new list names
3. Pass complete list to `contact_update`

#### List Labels
List all labels/lists in your Apollo account:
```python
labels_list()  # Get all labels (contacts, accounts, emailer_campaigns)
labels_list(modality="contacts")  # Get only contact lists
labels_list(modality="accounts")  # Get only account lists
```

**Note**: This endpoint requires a **master API key**. Regular API keys will receive a 403 error.

#### Bulk Create Contacts
Create up to 100 contacts in a single operation:
```python
contact_bulk_create(
    contacts=[
        {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "title": "Product Manager",
            "organization_name": "Test Corp",
            "label_names": ["Hot Leads"]
        },
        {
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob@testco.com",
            "title": "Engineer",
            "organization_name": "Test Company"
        }
    ]
)
```

Returns two arrays:
- `created_contacts`: Newly created contacts
- `existing_contacts`: Contacts that already existed (matched by email, **not updated**)

#### Bulk Update Contacts
Update up to 100 contacts in a single operation:
```python
contact_bulk_update(
    contacts=[
        {
            "id": "contact_id_1",
            "title": "Senior Product Manager",
            "label_names": ["Hot Leads", "Q1 2024"]
        },
        {
            "id": "contact_id_2",
            "email": "newemail@example.com"
        }
    ]
)
```

**Note**: Each contact must have an `id` field. Only provided fields will be updated.

#### Get Usage Stats
Monitor your API usage and rate limits:
```python
usage_stats()
```

Returns rate limits per endpoint with minute, hour, and day limits, plus consumed and remaining counts.

**Note**: This endpoint requires a **master API key**. Regular API keys will receive a 403 error.

### Account Management

#### Search Accounts
Search accounts (companies) you've saved to your Apollo CRM:
```python
account_search(
    query="apollo.io",  # Search by name, domain, etc.
    page=1,
    per_page=25
)
```

#### Create Account
Create a new account in your CRM:
```python
account_create(
    name="Apollo.io",
    domain="apollo.io",
    phone="+1-415-555-0100",
    label_names=["Enterprise", "Active"]
)
```

**Note**: Requires **master API key**.

#### Update Account
Update an existing account's information:
```python
account_update(
    account_id="account_123",
    phone="+1-415-555-0200",
    label_names=["Enterprise", "VIP"]  # REPLACES all existing labels
)
```

**Important**: `label_names` in `account_update` REPLACES all lists. Use the helper tools below to safely add/remove labels.

#### Add Accounts to List (Safely)
Add accounts to a list without losing existing labels:
```python
account_add_to_list(
    account_ids=["account_123", "account_456"],
    label_name="Q1 2024 Targets"
)
```

This helper tool:
1. Fetches current labels for each account
2. Merges the new label with existing labels
3. Performs bulk update with complete label list
4. Returns `found_ids`, `not_found_ids`, and `updated_accounts`

**Note**: Requires **master API key**.

#### Remove Accounts from List (Safely)
Remove accounts from a list while preserving other labels:
```python
account_remove_from_list(
    account_ids=["account_123", "account_456"],
    label_name="Q1 2024 Targets"
)
```

This helper tool:
1. Fetches current labels for each account
2. Removes only the specified label
3. Keeps all other labels intact
4. Performs bulk update

**Note**: Requires **master API key**.

#### Bulk Create Accounts
Create multiple accounts in a single operation:
```python
account_bulk_create(
    accounts=[
        {
            "name": "Company A",
            "domain": "companya.com",
            "label_names": ["Prospects"]
        },
        {
            "name": "Company B",
            "domain": "companyb.com",
            "label_names": ["Prospects"]
        }
    ]
)
```

Returns two arrays:
- `created_accounts`: Newly created accounts
- `existing_accounts`: Accounts that already existed (matched by domain)

**Note**: Requires **master API key**.

#### Bulk Update Accounts
Update multiple accounts in a single operation:
```python
account_bulk_update(
    accounts=[
        {
            "id": "account_123",
            "label_names": ["Enterprise", "Active", "Q1 Target"]
        },
        {
            "id": "account_456",
            "phone": "+1-555-0100"
        }
    ]
)
```

**Note**: Each account must have an `id` field. Only provided fields will be updated. Requires **master API key**.

## Data Models

The `apollo/` directory contains the data models for the Apollo.io API. These models are used to define the input and output of the MCP tools.

- `apollo/people.py`: Defines the data models for the People Enrichment endpoint and Contact model.
- `apollo/organization.py`: Defines the data models for the Organization Enrichment endpoint.
- `apollo/people_search.py`: Defines the data models for the People Search endpoint.
- `apollo/organization_search.py`: Defines the data models for the Organization Search endpoint.
- `apollo/organization_job_postings.py`: Defines the data models for the Organization Job Postings endpoint.
- `apollo/contacts.py`: Defines the data models for contact write operations (search, create, update, bulk create, bulk update).
- `apollo/accounts.py`: Defines the data models for account write operations (search, create, update, bulk operations).
- `apollo/labels.py`: Defines the data models for labels/lists operations.
- `apollo/usage_stats.py`: Defines the data models for API usage statistics and rate limits.

## Testing

The project has comprehensive test coverage across 3 categories:

### Unit Tests (31 tests)
Test apollo_client methods with mocked HTTP responses:
```bash
pytest tests/unit/
```

### Integration Tests (20 tests)
Test apollo_client methods with real API calls (VCR recorded):
```bash
pytest tests/integration/ -m integration
```

### Tool Tests (8 tests)
Test MCP tools end-to-end using `mcp.call_tool()`:
```bash
pytest tests/tools/ -m integration
```

**Run all tests:**
```bash
pytest tests/
```

**Note**: Integration tests require `APOLLO_IO_API_KEY` environment variable. Tool tests that modify data are skipped by default and require a master API key.

## Usage with Claude for Desktop

1. Configure Claude for Desktop to use these MCP servers by adding them to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "apollo-io-mcp-server": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "mcp",
        "run",
        "path/to/apollo-io-mcp-server/server.py"
      ]
    }
  }
}
```

## Resources

- [Apollo.io API Documentation](https://docs.apollo.io/reference/)
- [MCP Protocol Documentation](https://github.com/modelcontextprotocol/mcp)
- [Claude for Desktop Documentation](https://claude.ai/docs)
