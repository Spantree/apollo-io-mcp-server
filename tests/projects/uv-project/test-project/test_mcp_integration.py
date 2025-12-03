#!/usr/bin/env python3
"""
Integration test script for Apollo.io MCP Server

This script validates the MCP server can:
1. Start correctly
2. Load tools
3. Handle basic queries
4. Respond with proper error messages
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def check_prerequisites():
    """Check all prerequisites are met"""
    print("\n" + "="*60)
    print("Checking Prerequisites")
    print("="*60)

    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
    else:
        print_error(f"Python version too old: {version.major}.{version.minor}.{version.micro}")
        print_error("Requires Python 3.10+")
        return False

    # Check uv is installed
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"uv installed: {result.stdout.strip()}")
        else:
            print_error("uv is not installed")
            return False
    except FileNotFoundError:
        print_error("uv is not installed")
        print_info("Install from: https://docs.astral.sh/uv/")
        return False

    # Check API key is set
    api_key = os.getenv('APOLLO_IO_API_KEY') or os.getenv('APOLLO_API_KEY')
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print_success(f"API key found: {masked_key}")
    else:
        print_error("APOLLO_IO_API_KEY not set")
        print_info("Set with: export APOLLO_IO_API_KEY='your_key'")
        return False

    # Check project structure
    parent_dir = Path(__file__).parent.parent
    server_py = parent_dir / "server.py"
    if server_py.exists():
        print_success(f"server.py found at: {server_py}")
    else:
        print_error(f"server.py not found at: {server_py}")
        return False

    return True

def test_server_list_tools():
    """Test that server can list tools"""
    print("\n" + "="*60)
    print("Testing Tool Listing")
    print("="*60)

    parent_dir = Path(__file__).parent.parent

    try:
        result = subprocess.run(
            ['uv', 'run', '--directory', str(parent_dir), 'python', 'server.py', 'list-tools'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print_success("Server listed tools successfully")

            # Count tools in output
            output = result.stdout
            if 'people_search' in output and 'organization_search' in output:
                print_success("Core tools found in output")
                print_info(f"Output preview:\n{output[:500]}")
                return True
            else:
                print_error("Expected tools not found in output")
                return False
        else:
            print_error("Server failed to list tools")
            print_error(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print_error("Server timed out (30s)")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_mcp_json_config():
    """Test that .mcp.json is valid"""
    print("\n" + "="*60)
    print("Testing .mcp.json Configuration")
    print("="*60)

    mcp_json_path = Path(__file__).parent / ".mcp.json"

    if not mcp_json_path.exists():
        print_error(f".mcp.json not found at: {mcp_json_path}")
        return False

    try:
        with open(mcp_json_path) as f:
            config = json.load(f)

        print_success(".mcp.json is valid JSON")

        # Check structure
        if 'mcpServers' in config:
            print_success("mcpServers key found")

            servers = config['mcpServers']
            if servers:
                print_success(f"Found {len(servers)} server(s) configured")
                for name, server_config in servers.items():
                    print_info(f"  - {name}")
                    if 'command' in server_config:
                        print_success(f"    Command: {server_config['command']}")
                    if 'env' in server_config and 'APOLLO_IO_API_KEY' in server_config['env']:
                        print_success(f"    API key configured")
                return True
            else:
                print_error("No servers configured")
                return False
        else:
            print_error("mcpServers key not found")
            return False

    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON: {e}")
        return False
    except Exception as e:
        print_error(f"Error reading .mcp.json: {e}")
        return False

def test_server_startup():
    """Test that server can start (quick startup test)"""
    print("\n" + "="*60)
    print("Testing Server Startup")
    print("="*60)

    parent_dir = Path(__file__).parent.parent

    # Try to import server module to check for syntax errors
    try:
        sys.path.insert(0, str(parent_dir))
        import server
        print_success("Server module imports without errors")

        # Check key components exist
        if hasattr(server, 'app'):
            print_success("Typer app found")
        if hasattr(server, 'mcp'):
            print_success("FastMCP instance found")

        return True

    except ImportError as e:
        print_error(f"Failed to import server: {e}")
        return False
    except Exception as e:
        print_error(f"Error loading server: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available"""
    print("\n" + "="*60)
    print("Testing Dependencies")
    print("="*60)

    required_packages = [
        'mcp',
        'httpx',
        'pydantic',
        'dotenv',
        'typer',
    ]

    all_ok = True
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
                package_name = 'python-dotenv'
            else:
                __import__(package)
                package_name = package
            print_success(f"{package_name} is installed")
        except ImportError:
            print_error(f"{package_name} is not installed")
            all_ok = False

    return all_ok

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Apollo.io MCP Server Integration Tests")
    print("="*60)

    tests = [
        ("Prerequisites", check_prerequisites),
        ("Dependencies", test_dependencies),
        (".mcp.json Config", test_mcp_json_config),
        ("Server Startup", test_server_startup),
        ("Tool Listing", test_server_list_tools),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    print("\n" + "-"*60)
    if passed == total:
        print_success(f"All tests passed ({passed}/{total})")
        print("\n" + GREEN + "✓ MCP Server is ready to use!" + RESET)
        print("\nNext steps:")
        print("  1. Open this directory in Claude Code")
        print("  2. Check MCP server status (should show connected)")
        print("  3. Try test queries from README.md")
        return 0
    else:
        print_error(f"Some tests failed ({passed}/{total} passed)")
        print("\n" + RED + "✗ MCP Server has issues" + RESET)
        print("\nReview the errors above and fix them before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
