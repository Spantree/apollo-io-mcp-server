# Apollo.io MCP Server Tests

This directory contains comprehensive tests for the Apollo.io MCP server.

## Directory Structure

```
test/
├── README.md                    # This file
└── projects/
    ├── uv-project/              # Local development testing
    │   ├── .mcp.json.example    # Local server config
    │   ├── README.md            # Setup instructions
    │   ├── SUMMARY.md           # Quick reference
    │   ├── test_mcp_integration.py  # Automated tests
    │   └── test-queries.md      # Manual test queries
    └── uvx-project/             # Production installation testing
        ├── .mcp.json.example    # GitHub server config
        └── README.md            # Setup instructions
```

## Test Projects

### UV Project (Development)

**Location:** `test/projects/uv-project/`
**Purpose:** Test local development workflow
**Method:** Runs server from local repository using `uv`

**Use when:**
- Developing new features
- Testing local changes
- Debugging issues
- Before pushing to GitHub

**Quick start:**
```bash
cd test/projects/uv-project
cp .mcp.json.example .mcp.json
claude mcp get apollo-io-uv
```

### UVX Project (Production)

**Location:** `test/projects/uvx-project/`
**Purpose:** Test production installation experience
**Method:** Installs from GitHub using `uvx`

**Use when:**
- Validating GitHub releases
- Testing end-user experience
- Verifying production setup
- After pushing to GitHub

**Quick start:**
```bash
cd test/projects/uvx-project
cp .mcp.json.example .mcp.json
claude mcp get apollo-io-uvx
```

## Running Tests

### Automated Tests

Run the integration test suite:

```bash
cd test/projects/uv-project
python test_mcp_integration.py
```

Expected: All 5 tests pass
- ✅ Prerequisites check
- ✅ Dependencies verification
- ✅ .mcp.json configuration
- ✅ Server startup
- ✅ Tool listing

### Manual Tests

Test with Claude Code CLI:

```bash
# Test local development setup
cd test/projects/uv-project
claude mcp get apollo-io-uv

# Test production setup
cd test/projects/uvx-project
claude mcp get apollo-io-uvx
```

Both should show:
- Status: ✓ Connected
- Tools: 20 tools available

### Full Test Workflow

1. **Local development test:**
   ```bash
   cd test/projects/uv-project
   python test_mcp_integration.py
   claude mcp get apollo-io-uv
   ```

2. **Make changes** to server code

3. **Test changes locally:**
   ```bash
   cd test/projects/uv-project
   claude mcp get apollo-io-uv
   # Changes should reflect immediately
   ```

4. **Commit and push** to GitHub

5. **Test production installation:**
   ```bash
   cd test/projects/uvx-project
   # Clear cache to get latest
   rm -rf ~/.local/share/uv/tools/apollo-io-mcp-server
   claude mcp get apollo-io-uvx
   ```

## Test Queries

For detailed manual testing, see:
- `test/projects/uv-project/test-queries.md` - 24 comprehensive test queries

Categories:
- People tools (3 queries)
- Organization tools (3 queries)
- Contact management (5 queries)
- Account management (3 queries)
- Utility tools (3 queries)
- Error handling (3 queries)
- Performance (2 queries)
- Integration (2 queries)

## Prerequisites

- Python 3.10+
- `uv` package manager
- Apollo.io API key
- Claude Code CLI

## Environment Setup

```bash
# Set API key
export APOLLO_IO_API_KEY="your_api_key_here"

# Verify
echo $APOLLO_IO_API_KEY
```

## Troubleshooting

### Both Projects Fail

**Check API key:**
```bash
echo $APOLLO_IO_API_KEY
```

**Check uv/uvx:**
```bash
uv --version
uvx --version
```

### UV Project Fails

**Install dependencies:**
```bash
cd ../../..
uv sync
```

**Test manually:**
```bash
uv run python server.py list-tools
```

### UVX Project Fails

**Clear cache:**
```bash
rm -rf ~/.local/share/uv/tools/apollo-io-mcp-server
```

**Test installation:**
```bash
uvx --from git+https://github.com/Spantree/apollo-io-mcp-server.git apollo-io-mcp-server list-tools
```

### Claude MCP Command Issues

**List configured servers:**
```bash
claude mcp list
```

**Check specific server:**
```bash
claude mcp get apollo-io-uv
claude mcp get apollo-io-uvx
```

## Success Criteria

### UV Project
- [x] Dependencies install via `uv sync`
- [x] Automated tests pass (5/5)
- [ ] `claude mcp get apollo-io-uv` shows connected
- [ ] All 20 tools available
- [ ] Can execute queries in Claude Code

### UVX Project
- [ ] Installs from GitHub via uvx
- [ ] `claude mcp get apollo-io-uvx` shows connected
- [ ] All 20 tools available
- [ ] Can execute queries in Claude Code
- [ ] Updates automatically on cache clear

## CI/CD Integration

Future: Add GitHub Actions workflow to:
1. Run automated tests on push
2. Test both uv and uvx methods
3. Validate all 20 tools load
4. Run test queries
5. Report results

## Contributing

When adding new features:
1. Test in `uv-project` first
2. Update `test_mcp_integration.py` if needed
3. Add test queries to `test-queries.md`
4. Verify in `uvx-project` after pushing
5. Update documentation

## Notes

- UV project tests **development workflow**
- UVX project tests **user experience**
- Both should pass for a successful release
- Keep test projects in sync with main codebase
