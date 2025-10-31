# Testing the Apollo.io MCP Server

This guide shows you how to test the new bulk operations and usage stats features.

## Quick Start

### 1. MCP Inspector (Interactive Testing) ✨

**Currently running at:**
```
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=3ebdeae018debb6e27138a6ca8f7cad3f89a67fc17d25c9057cc30c0a2a042ce
```

Open this URL to:
- Browse all 12 MCP tools
- Test `contact_bulk_create`, `contact_bulk_update`, and `usage_stats`
- Try sample requests without writing code
- View JSON requests/responses

To start inspector again later:
```bash
npx @modelcontextprotocol/inspector uv run mcp run server.py
```

### 2. Unit Tests (No API Key Required)

Run the mocked unit tests:
```bash
# All contact tests
pytest tests/test_unit_contacts.py -v

# Just the new tests
pytest tests/test_unit_contacts.py::test_contact_bulk_create_unit -v
pytest tests/test_unit_contacts.py::test_contact_bulk_update_unit -v
pytest tests/test_unit_contacts.py::test_usage_stats_unit -v
```

### 3. Test Script (With Real API)

Run the local test script:
```bash
# Without API key (shows examples only)
uv run python test_local.py

# With API key (creates real test contacts!)
export APOLLO_IO_API_KEY="your_key_here"
uv run python test_local.py
```

This will:
- ✅ Get usage stats (requires master API key)
- ✅ Bulk create 2 test contacts
- ✅ Bulk update those contacts

### 4. Claude Code (Test with AI)

The MCP server is already configured in `.claude/claude_code.json`!

**To use it:**

1. Make sure your API key is set:
   ```bash
   export APOLLO_IO_API_KEY="your_key_here"
   ```

2. Ask Claude Code to use the tools:
   ```
   "Can you use the contact_bulk_create tool to create 3 test contacts?"

   "Can you check my API usage stats with usage_stats?"

   "Can you bulk update these contacts: [provide IDs]"
   ```

3. Claude Code will automatically discover and use the MCP tools!

## Tool Examples

### contact_bulk_create
```json
{
  "contacts": [
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
      "email": "bob@testco.com"
    }
  ]
}
```

Returns:
- `created_contacts`: Array of newly created contacts
- `existing_contacts`: Array of contacts that already existed (not updated)

### contact_bulk_update
```json
{
  "contacts": [
    {
      "id": "contact_id_1",
      "title": "Senior Product Manager"
    },
    {
      "id": "contact_id_2",
      "email": "newemail@example.com"
    }
  ]
}
```

### usage_stats
```json
{}
```

Returns rate limits per endpoint (requires master API key):
```json
{
  "api/v1/contacts/search": {
    "minute": {"limit": 60, "consumed": 5, "left_over": 55},
    "hour": {"limit": 600, "consumed": 42, "left_over": 558},
    "day": {"limit": 5000, "consumed": 234, "left_over": 4766}
  }
}
```

## Tips

- **MCP Inspector** is best for quick interactive testing
- **Unit tests** verify the code works correctly
- **Test script** tests with real API (careful, creates real data!)
- **Claude Code** tests the full AI integration

## Troubleshooting

### "403 Forbidden" on usage_stats
- This endpoint requires a **master API key**, not a regular API key
- Get a master key from Apollo.io settings

### MCP Inspector won't start
- Check if port 6274 is already in use
- Kill any existing inspector processes
- Try running again

### Claude Code doesn't see tools
- Restart Claude Code after adding MCP config
- Check that APOLLO_IO_API_KEY is in your environment
- Verify the path in `.claude/claude_code.json` is correct
