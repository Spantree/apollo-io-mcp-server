"""Main entry point for apollo-io-mcp-server"""
import sys
from server import app

def main():
    """Main entry point"""
    app()

if __name__ == "__main__":
    sys.exit(main())
