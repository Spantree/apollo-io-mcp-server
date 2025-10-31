from mcp.server.fastmcp import FastMCP
from apollo_client import ApolloClient
import os
import sys

from dotenv import load_dotenv
load_dotenv()
# Also load .env.secrets if present
load_dotenv('.env.secrets')

# Support both APOLLO_IO_API_KEY (preferred) and APOLLO_API_KEY
api_key = os.getenv("APOLLO_IO_API_KEY") or os.getenv("APOLLO_API_KEY")
apollo_client = ApolloClient(api_key=api_key)

mcp = FastMCP("Apollo.io")

# Parse command-line arguments for selective tool loading
# Usage: --tools people,organizations,contacts,accounts,misc
# Or specific tools: --tools people_search,organization_enrichment
enabled_categories = set()
enabled_tools = set()

if '--tools' in sys.argv:
    try:
        tools_idx = sys.argv.index('--tools')
        tools_arg = sys.argv[tools_idx + 1]
        tool_list = [t.strip() for t in tools_arg.split(',')]

        # Categorize into categories vs specific tools
        categories = {'people', 'organizations', 'contacts', 'accounts', 'misc'}
        for tool in tool_list:
            if tool in categories:
                enabled_categories.add(tool)
            else:
                enabled_tools.add(tool)

        print(f"[Apollo MCP] Loading tools: categories={enabled_categories}, specific={enabled_tools}", file=sys.stderr)
    except (IndexError, ValueError) as e:
        print(f"[Apollo MCP] Error parsing --tools argument: {e}", file=sys.stderr)
        print("[Apollo MCP] Usage: --tools people,organizations,contacts,accounts,misc", file=sys.stderr)
        print("[Apollo MCP] Or specific: --tools people_search,organization_enrichment", file=sys.stderr)
else:
    # Load all tools by default
    enabled_categories = {'people', 'organizations', 'contacts', 'accounts', 'misc'}

# Register tools from modular tool files based on selection
from tools import people, organizations, contacts, accounts, misc

if 'people' in enabled_categories or any(t.startswith('people_') for t in enabled_tools):
    people.register_tools(mcp, apollo_client)

if 'organizations' in enabled_categories or any(t.startswith('organization_') for t in enabled_tools):
    organizations.register_tools(mcp, apollo_client)

if 'contacts' in enabled_categories or any(t.startswith('contact_') for t in enabled_tools):
    contacts.register_tools(mcp, apollo_client)

if 'accounts' in enabled_categories or any(t.startswith('account_') for t in enabled_tools):
    accounts.register_tools(mcp, apollo_client)

if 'misc' in enabled_categories or any(t in ['labels_list', 'usage_stats'] for t in enabled_tools):
    misc.register_tools(mcp, apollo_client)

# if __name__ == "__main__":
#     mcp.run(transport="stdio")
