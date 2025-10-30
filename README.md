# Apollo.io MCP Server

This project provides an MCP server that exposes the Apollo.io API functionalities as tools. It allows you to interact with the Apollo.io API using the Model Context Protocol (MCP).

## Overview

The project consists of the following main components:

- `apollo_client.py`: Defines the `ApolloClient` class, which is used to interact with the Apollo.io API. It includes methods for people enrichment, organization enrichment, people search, organization search, organization job postings, and contact management (search, create, update).
- `server.py`: Defines the FastMCP server, which exposes the Apollo.io API functionalities as tools. It uses the `ApolloClient` class defined in `apollo_client.py` to interact with the API.
- `apollo/`: Contains the data models for the Apollo.io API, such as `PeopleEnrichmentQuery`, `OrganizationEnrichmentQuery`, `PeopleSearchQuery`, `OrganizationSearchQuery`, `OrganizationJobPostingsQuery`, and contact models for write operations.

## Functionalities

The following functionalities are exposed as MCP tools:

### Read Operations (Prospecting & Enrichment)

-   `people_enrichment`: Use the People Enrichment endpoint to enrich data for 1 person.
-   `organization_enrichment`: Use the Organization Enrichment endpoint to enrich data for 1 company.
-   `people_search`: Use the People Search endpoint to find people in Apollo's global database (275M+ people).
-   `organization_search`: Use the Organization Search endpoint to find organizations.
-   `organization_job_postings`: Use the Organization Job Postings endpoint to find job postings for a specific organization.

### Write Operations (Contact Management)

-   `contact_search`: Search contacts saved to YOUR Apollo CRM (not global search). Returns `contact_id` needed for updates.
-   `contact_create`: Create a new contact in your Apollo CRM with optional list assignment.
-   `contact_update`: Update an existing contact in your Apollo CRM, including managing list membership.
-   `labels_list`: List all labels/lists in your Apollo account, with optional filtering by modality (contacts, accounts, emailer_campaigns). **Requires master API key.**

**Note on Lists vs Labels**: Apollo's API uses the term "labels" (via `label_names` parameter), but these appear as "Lists" in the Apollo UI. They are the same thing. Lists can be automatically created when you assign contacts to them.

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

## Data Models

The `apollo/` directory contains the data models for the Apollo.io API. These models are used to define the input and output of the MCP tools.

- `apollo/people.py`: Defines the data models for the People Enrichment endpoint and Contact model.
- `apollo/organization.py`: Defines the data models for the Organization Enrichment endpoint.
- `apollo/people_search.py`: Defines the data models for the People Search endpoint.
- `apollo/organization_search.py`: Defines the data models for the Organization Search endpoint.
- `apollo/organization_job_postings.py`: Defines the data models for the Organization Job Postings endpoint.
- `apollo/contacts.py`: Defines the data models for contact write operations (search, create, update).
- `apollo/labels.py`: Defines the data models for labels/lists operations.

## Testing

To test, set `APOLLO_IO_API_KEY` environment variable and run `uv run apollo_client.py`.

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
