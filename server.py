from mcp.server.fastmcp import FastMCP
from apollo_client import ApolloClient
import os

from dotenv import load_dotenv
load_dotenv()
# Also load .env.secrets if present
load_dotenv('.env.secrets')

# Support both APOLLO_API_KEY and APOLLO_IO_API_KEY
api_key = os.getenv("APOLLO_API_KEY") or os.getenv("APOLLO_IO_API_KEY")
apollo_client = ApolloClient(api_key=api_key)

mcp = FastMCP("Apollo.io")

# Register all tools from modular tool files
from tools import people, organizations, contacts, accounts, misc

people.register_tools(mcp, apollo_client)
organizations.register_tools(mcp, apollo_client)
contacts.register_tools(mcp, apollo_client)
accounts.register_tools(mcp, apollo_client)
misc.register_tools(mcp, apollo_client)

# if __name__ == "__main__":
#     mcp.run(transport="stdio")
