# Apollo.io MCP Server Test Project

This test project validates that the Apollo.io MCP server works correctly with Claude Code.

## Setup

### 1. Ensure API Key is Set

```bash
# Check if API key is set
echo $APOLLO_IO_API_KEY

# If not set, add it:
export APOLLO_IO_API_KEY="your_api_key_here"
```

### 2. Install Dependencies (for local testing)

```bash
cd ..
uv sync
cd test-project
```

## Testing Methods

### Method 1: Test with Claude Code (Recommended)

1. Open this `test-project` directory in Claude Code
2. Claude Code will automatically detect `.mcp.json` and load the MCP server
3. Check the MCP server status indicator - should show "apollo-io-local" as connected
4. Try the test queries below in Claude Code

### Method 2: Test with MCP CLI

Test the server directly using the MCP CLI:

```bash
# List available tools
uv run --directory .. python server.py list-tools

# Test server starts correctly
uv run --directory .. mcp dev server.py

# In another terminal, you can use mcp-client to test
```

### Method 3: Manual Integration Test

Use the test script:

```bash
python test_mcp_integration.py
```

## Test Queries for Claude Code

Once the MCP server is loaded in Claude Code, try these queries:

### Basic Connectivity Test
```
List all available Apollo.io tools
```

Expected: Should return list of 20+ tools (people, organizations, contacts, accounts, misc)

### People Search Test
```
Search Apollo for software engineers at startups in San Francisco.
Show me the top 3 results.
```

Expected: Should use `people_search` tool and return results

### Organization Search Test
```
Search for SaaS companies in Austin, Texas with 50-200 employees.
Show me 5 results.
```

Expected: Should use `organization_search` tool and return results

### Tool Filtering Test

Edit `.mcp.json` to test selective tool loading:

```json
{
  "mcpServers": {
    "apollo-io-limited": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "..",
        "python",
        "server.py",
        "--include-tools=people_search,organization_search"
      ],
      "env": {
        "APOLLO_IO_API_KEY": "${env:APOLLO_IO_API_KEY}"
      }
    }
  }
}
```

Restart Claude Code and verify only 2 tools are loaded.

## Expected Results

### Successful Connection
- ✅ MCP server shows as "connected" in Claude Code
- ✅ Apollo.io tools appear in tool list
- ✅ No connection errors in console

### Tool Execution
- ✅ Search tools return results
- ✅ Results are properly formatted
- ✅ Rate limiting works (no 429 errors)
- ✅ Error messages are clear if API key is invalid

### Performance
- ✅ Server starts in < 3 seconds
- ✅ Tool calls respond in < 5 seconds
- ✅ No memory leaks or crashes

## Troubleshooting

### Server Won't Start

**Check Python version:**
```bash
python --version
# Should be 3.10+
```

**Check dependencies:**
```bash
cd .. && uv sync
```

**Check API key:**
```bash
echo $APOLLO_IO_API_KEY
# Should print your API key (not empty)
```

**Check logs:**
Look at Claude Code console for error messages

### Tools Not Appearing

**Verify .mcp.json syntax:**
```bash
cat .mcp.json | python -m json.tool
# Should parse without errors
```

**Check server is running:**
- Look for "apollo-io-local" in MCP server list
- Should show green/connected status

### API Errors

**403 Forbidden:**
- Some tools require master API key
- Contact Apollo.io support for master key

**429 Too Many Requests:**
- Rate limiting is working
- Wait for rate limit window to reset
- Or adjust rate limits in environment

**401 Unauthorized:**
- API key is invalid or expired
- Get new key from Apollo.io settings

## Configuration Options

### Test with Selective Tools

**Prospecting only:**
```json
"args": [
  "run", "--directory", "..",
  "python", "server.py",
  "--include-tools=people_search,people_enrichment,organization_search"
]
```

**With rate limit customization:**
```json
"args": [
  "run", "--directory", "..",
  "python", "server.py",
  "--rate-limit-min", "100"
]
```

**Disable rate limiting (testing only):**
```json
"env": {
  "APOLLO_IO_API_KEY": "${env:APOLLO_IO_API_KEY}",
  "APOLLO_MCP_NO_RATE_LIMIT": "true"
}
```

## Success Criteria

All these should pass:
- [ ] Server starts without errors
- [ ] Claude Code connects to server
- [ ] All 20 tools are available (or filtered count if using --include-tools)
- [ ] `people_search` returns results
- [ ] `organization_search` returns results
- [ ] Rate limiting prevents 429 errors
- [ ] Error messages are clear and helpful
- [ ] Server handles invalid queries gracefully

## Next Steps

After validation:
1. Test with uvx (production installation method)
2. Test selective tool loading
3. Test rate limiting behavior
4. Test error handling
5. Performance testing with bulk operations

## Testing with uvx (Production Install)

To test the actual installation method users will use:

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

This tests the actual production installation path.
