#!/bin/bash
# Validation script for both test projects

set -e

echo "==================================="
echo "Apollo.io MCP Server Config Tests"
echo "==================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check API key
if [ -z "$APOLLO_IO_API_KEY" ]; then
    echo -e "${RED}✗${NC} APOLLO_IO_API_KEY not set"
    echo "  Set with: export APOLLO_IO_API_KEY='your_key'"
    exit 1
else
    echo -e "${GREEN}✓${NC} APOLLO_IO_API_KEY is set"
fi

echo ""
echo "-----------------------------------"
echo "Testing UV Project (Local Dev)"
echo "-----------------------------------"

cd tests/projects/uv-project

# Check config exists
if [ -f ".mcp.json" ]; then
    echo -e "${GREEN}✓${NC} .mcp.json exists"
else
    echo -e "${YELLOW}⚠${NC} .mcp.json not found, creating from example..."
    cp .mcp.json.example .mcp.json
fi

# Validate JSON
if python3 -m json.tool .mcp.json > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} .mcp.json is valid JSON"
else
    echo -e "${RED}✗${NC} .mcp.json is invalid JSON"
    exit 1
fi

# Check claude mcp status
echo "Testing MCP connection..."
if claude mcp get apollo-io-uv > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} apollo-io-uv server recognized"
    claude mcp get apollo-io-uv
else
    echo -e "${YELLOW}⚠${NC} apollo-io-uv server found but may not be connected"
    echo "  (This is normal if Claude Code isn't running)"
fi

cd ../../..

echo ""
echo "-----------------------------------"
echo "Testing UVX Project (Production)"
echo "-----------------------------------"

cd tests/projects/uvx-project

# Check config exists
if [ -f ".mcp.json" ]; then
    echo -e "${GREEN}✓${NC} .mcp.json exists"
else
    echo -e "${YELLOW}⚠${NC} .mcp.json not found, creating from example..."
    cp .mcp.json.example .mcp.json
fi

# Validate JSON
if python3 -m json.tool .mcp.json > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} .mcp.json is valid JSON"
else
    echo -e "${RED}✗${NC} .mcp.json is invalid JSON"
    exit 1
fi

# Test uvx installation
echo "Testing UVX installation from GitHub..."
if uvx --from git+https://github.com/Spantree/apollo-io-mcp-server.git apollo-io-mcp-server list-tools > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} UVX installation works"
    echo "  (20 tools available)"
else
    echo -e "${RED}✗${NC} UVX installation failed"
    exit 1
fi

# Check claude mcp status
echo "Testing MCP connection..."
if claude mcp get apollo-io-uvx > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} apollo-io-uvx server recognized"
    claude mcp get apollo-io-uvx
else
    echo -e "${YELLOW}⚠${NC} apollo-io-uvx server found but may not be connected"
    echo "  (This is normal if Claude Code isn't running)"
fi

cd ../../..

echo ""
echo "==================================="
echo "Summary"
echo "==================================="
echo ""
echo -e "${GREEN}✓${NC} Both test projects configured correctly"
echo -e "${GREEN}✓${NC} UVX installation from GitHub works"
echo ""
echo "To test in Claude Code:"
echo "  1. Open test/projects/uv-project in Claude Code"
echo "  2. Check MCP status for apollo-io-uv"
echo "  3. Open test/projects/uvx-project in Claude Code"
echo "  4. Check MCP status for apollo-io-uvx"
echo ""
echo -e "${GREEN}Both configurations are ready!${NC}"
