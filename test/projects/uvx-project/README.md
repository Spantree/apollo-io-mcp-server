# UVX Test Project

This test project validates the **production installation method** using `uvx` to install directly from GitHub.

## Purpose

Tests that users can install and use the Apollo.io MCP server with **zero manual installation** - just configure `.mcp.json` and restart Claude Code.

## Configuration

This project uses the production installation method:

```json
{
  "mcpServers": {
    "apollo-io-uvx": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Spantree/apollo-io-mcp-server.git",
        "apollo-io-mcp-server",
        "mcp"
      ],
      "env": {
        "APOLLO_IO_API_KEY": "${env:APOLLO_IO_API_KEY}"
      }
    }
  }
}
```

## Setup

### 1. Set API Key

```bash
export APOLLO_IO_API_KEY="your_api_key_here"
```

### 2. Create Local Config

```bash
cp .mcp.json.example .mcp.json
```

### 3. Test Installation

```bash
# Test that uvx can install and run
uvx --from git+https://github.com/Spantree/apollo-io-mcp-server.git apollo-io-mcp-server list-tools
```

### 4. Test with Claude Code

```bash
# From this directory
claude mcp get apollo-io-uvx
```

Expected: Shows server as connected with all 20 tools available.

## What This Tests

✅ **GitHub Installation** - Installs directly from GitHub
✅ **uvx Package Resolution** - Resolves dependencies automatically
✅ **Entry Point** - Tests `apollo-io-mcp-server` command
✅ **Module Loading** - Verifies all modules import correctly
✅ **Tool Registration** - Confirms all 20 tools are registered
✅ **Environment Variables** - API key passed correctly

## Comparison with UV Project

**This Project (uvx-project):**
- Installs from GitHub
- Uses production installation method
- Tests what end users will experience
- No local repository needed

**UV Project (uv-project):**
- Runs from local repository
- Uses development installation method
- Tests local changes before pushing
- Requires repository clone

## Success Criteria

- [ ] `uvx` installs package from GitHub
- [ ] All 20 tools load successfully
- [ ] `claude mcp get apollo-io-uvx` shows connected
- [ ] No import errors
- [ ] Environment variables work
- [ ] Can execute tool queries in Claude Code

## Troubleshooting

### Server Won't Connect

**Check installation:**
```bash
uvx --from git+https://github.com/Spantree/apollo-io-mcp-server.git apollo-io-mcp-server list-tools
```

**Clear cache:**
```bash
rm -rf ~/.local/share/uv/tools/apollo-io-mcp-server
```

### API Key Issues

```bash
echo $APOLLO_IO_API_KEY
# Should print your key
```

### Check Server Status

```bash
claude mcp get apollo-io-uvx
```

Shows connection status and any errors.

## Expected Output

```bash
$ claude mcp get apollo-io-uvx
apollo-io-uvx:
  Scope: Project config (shared via .mcp.json)
  Status: ✓ Connected
  Tools: 20 tools available

  PEOPLE (3):
    - people_enrichment
    - people_bulk_enrichment
    - people_search

  ORGANIZATIONS (3):
    - organization_enrichment
    - organization_search
    - organization_job_postings

  CONTACTS (5):
    - contact_search
    - contact_create
    - contact_update
    - contact_bulk_create
    - contact_bulk_update

  ACCOUNTS (7):
    - account_search
    - account_create
    - account_update
    - account_bulk_create
    - account_bulk_update
    - account_add_to_list
    - account_remove_from_list

  MISC (2):
    - labels_list
    - usage_stats
```

## Notes

- This is the **recommended installation method** for end users
- Updates automatically when you restart Claude Code
- No manual `pip install` or `uv pip install` needed
- Clean, simple configuration
