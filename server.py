from mcp.server.fastmcp import FastMCP
from apollo_client import ApolloClient
import os
import sys
import typer
from typing import Optional

from dotenv import load_dotenv
load_dotenv()
# Also load .env.secrets if present
load_dotenv('.env.secrets')

# All available tools organized by category
ALL_TOOLS = {
    'people': ['people_enrichment', 'people_bulk_enrichment', 'people_search'],
    'organizations': ['organization_enrichment', 'organization_search', 'organization_job_postings'],
    'contacts': ['contact_search', 'contact_create', 'contact_update', 'contact_bulk_create', 'contact_bulk_update'],
    'accounts': ['account_search', 'account_create', 'account_update', 'account_bulk_create', 'account_bulk_update', 'account_add_to_list', 'account_remove_from_list'],
    'misc': ['labels_list', 'usage_stats'],
}

# Flat list of all tool names
ALL_TOOL_NAMES = [tool for tools in ALL_TOOLS.values() for tool in tools]

# Tool name to category mapping
TOOL_TO_CATEGORY = {tool: cat for cat, tools in ALL_TOOLS.items() for tool in tools}

app = typer.Typer(
    name="apollo-io-mcp-server",
    help="Apollo.io MCP Server - Expose Apollo.io API as MCP tools",
    add_completion=False,
    no_args_is_help=False,
    invoke_without_command=True,
)


def parse_tool_list(tools_str: Optional[str]) -> list:
    """Parse comma-separated tool names."""
    if not tools_str:
        return []
    return [t.strip() for t in tools_str.split(',') if t.strip()]


def determine_enabled_tools(
    include: Optional[str] = None,
    exclude: Optional[str] = None
) -> set:
    """
    Determine which tools to enable based on include/exclude lists.

    Args:
        include: Comma-separated tool names to include (None = all tools)
        exclude: Comma-separated tool names to exclude

    Returns:
        Set of tool names to enable
    """
    include_list = parse_tool_list(include)
    exclude_list = parse_tool_list(exclude)

    # Start with all tools or only included tools
    if include_list:
        # Validate all included tools exist
        invalid_tools = [t for t in include_list if t not in ALL_TOOL_NAMES]
        if invalid_tools:
            typer.echo(f"[Apollo MCP] Error: Unknown tools: {', '.join(invalid_tools)}", err=True)
            typer.echo(f"[Apollo MCP] Run 'python server.py list-tools' to see available tools", err=True)
            raise typer.Exit(1)
        enabled_tools = set(include_list)
    else:
        enabled_tools = set(ALL_TOOL_NAMES)

    # Remove excluded tools
    if exclude_list:
        # Validate all excluded tools exist (just warning, not fatal)
        invalid_tools = [t for t in exclude_list if t not in ALL_TOOL_NAMES]
        if invalid_tools:
            typer.echo(f"[Apollo MCP] Warning: Unknown excluded tools: {', '.join(invalid_tools)}", err=True)
        enabled_tools -= set(exclude_list)

    return enabled_tools


def register_tools_from_set(mcp, apollo_client, enabled_tools: set):
    """Register only the specified tools with the MCP server."""
    from tools import people, organizations, contacts, accounts, misc

    # Determine which categories have at least one enabled tool
    enabled_categories = {TOOL_TO_CATEGORY[tool] for tool in enabled_tools}

    # Register tools by category
    if 'people' in enabled_categories:
        people.register_tools(mcp, apollo_client)

    if 'organizations' in enabled_categories:
        organizations.register_tools(mcp, apollo_client)

    if 'contacts' in enabled_categories:
        contacts.register_tools(mcp, apollo_client)

    if 'accounts' in enabled_categories:
        accounts.register_tools(mcp, apollo_client)

    if 'misc' in enabled_categories:
        misc.register_tools(mcp, apollo_client)


@app.command()
def list_tools(
    include_tools: Optional[str] = typer.Option(
        None,
        "--include-tools",
        help="Filter to show only these tools (comma-separated)"
    ),
    exclude_tools: Optional[str] = typer.Option(
        None,
        "--exclude-tools",
        help="Filter to exclude these tools (comma-separated)"
    )
):
    """List all available tools organized by category."""
    # Determine which tools to show
    enabled_tools = determine_enabled_tools(include_tools, exclude_tools)

    typer.echo("\n[Apollo.io MCP Server] Available Tools:\n")

    total = 0
    for category, tools in ALL_TOOLS.items():
        # Filter tools in this category
        visible_tools = [t for t in tools if t in enabled_tools]
        if not visible_tools:
            continue

        typer.echo(f"  {category.upper()} ({len(visible_tools)} tools):")
        for tool in visible_tools:
            typer.echo(f"    - {tool}")
        typer.echo()
        total += len(visible_tools)

    typer.echo(f"Total: {total} tools\n")

    if include_tools or exclude_tools:
        typer.echo("Showing filtered tools based on your --include-tools/--exclude-tools options\n")

    typer.echo("Usage:")
    typer.echo("  # Start server with all tools")
    typer.echo("  uv run mcp run server.py")
    typer.echo()
    typer.echo("  # Start server with specific tools")
    typer.echo("  uv run mcp run server.py --include-tools=people_search,organization_enrichment")
    typer.echo()
    typer.echo("  # Start server excluding specific tools")
    typer.echo("  uv run mcp run server.py --exclude-tools=account_bulk_create,account_bulk_update")
    typer.echo()


@app.command()
def mcp(
    include_tools: Optional[str] = typer.Option(
        None,
        "--include-tools",
        help="Comma-separated list of tool names to include (default: all tools)"
    ),
    exclude_tools: Optional[str] = typer.Option(
        None,
        "--exclude-tools",
        help="Comma-separated list of tool names to exclude"
    )
):
    """Start the Apollo.io MCP server."""
    # Determine enabled tools
    enabled_tools = determine_enabled_tools(include_tools, exclude_tools)

    if not enabled_tools:
        typer.echo("[Apollo MCP] Error: No tools enabled. Check your --include-tools/--exclude-tools filters.", err=True)
        raise typer.Exit(1)

    # Show what's being loaded
    if include_tools:
        typer.echo(f"[Apollo MCP] Including tools: {', '.join(sorted(enabled_tools))}", err=True)
    elif exclude_tools:
        typer.echo(f"[Apollo MCP] Excluding: {exclude_tools}", err=True)
        typer.echo(f"[Apollo MCP] Loading {len(enabled_tools)} tools", err=True)
    else:
        typer.echo(f"[Apollo MCP] Loading all {len(enabled_tools)} tools", err=True)

    # Support both APOLLO_IO_API_KEY (preferred) and APOLLO_API_KEY
    api_key = os.getenv("APOLLO_IO_API_KEY") or os.getenv("APOLLO_API_KEY")
    apollo_client = ApolloClient(api_key=api_key)

    mcp_instance = FastMCP("Apollo.io")

    # Register tools
    register_tools_from_set(mcp_instance, apollo_client, enabled_tools)

    # Store mcp globally for FastMCP CLI
    globals()['mcp'] = mcp_instance


@app.callback(invoke_without_command=True)
def default_command(
    ctx: typer.Context,
    include_tools: Optional[str] = typer.Option(
        None,
        "--include-tools",
        help="Comma-separated list of tool names to include (default: all tools)"
    ),
    exclude_tools: Optional[str] = typer.Option(
        None,
        "--exclude-tools",
        help="Comma-separated list of tool names to exclude"
    )
):
    """Default to 'mcp' command if no subcommand is specified."""
    if ctx.invoked_subcommand is None:
        # No subcommand was provided - run mcp command with these options
        ctx.invoke(mcp, include_tools=include_tools, exclude_tools=exclude_tools)


if __name__ == "__main__":
    # Direct execution - run Typer app
    app()
else:
    # For FastMCP compatibility when run via `mcp run server.py`
    # Parse sys.argv for --include-tools and --exclude-tools options
    include_arg = None
    exclude_arg = None

    for i, arg in enumerate(sys.argv):
        if arg.startswith('--include-tools='):
            include_arg = arg.split('=', 1)[1]
        elif arg == '--include-tools' and i + 1 < len(sys.argv):
            include_arg = sys.argv[i + 1]
        elif arg.startswith('--exclude-tools='):
            exclude_arg = arg.split('=', 1)[1]
        elif arg == '--exclude-tools' and i + 1 < len(sys.argv):
            exclude_arg = sys.argv[i + 1]

    # Determine enabled tools
    try:
        enabled_tools = determine_enabled_tools(include_arg, exclude_arg)
    except:
        enabled_tools = set(ALL_TOOL_NAMES)  # Fallback to all tools on error

    # Show what's being loaded
    if include_arg:
        typer.echo(f"[Apollo MCP] Including tools: {', '.join(sorted(enabled_tools))}", err=True)
    elif exclude_arg:
        typer.echo(f"[Apollo MCP] Excluding: {exclude_arg}", err=True)
        typer.echo(f"[Apollo MCP] Loading {len(enabled_tools)} tools", err=True)
    else:
        typer.echo(f"[Apollo MCP] Loading all {len(enabled_tools)} tools", err=True)

    # Initialize
    api_key = os.getenv("APOLLO_IO_API_KEY") or os.getenv("APOLLO_API_KEY")
    apollo_client = ApolloClient(api_key=api_key)
    mcp = FastMCP("Apollo.io")

    # Register tools
    register_tools_from_set(mcp, apollo_client, enabled_tools)
