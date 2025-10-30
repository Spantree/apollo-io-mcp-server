# Publishing to PyPI

This document provides instructions for publishing the apollo-io-mcp-server to PyPI.

## Prerequisites

1. Install `uv` if not already installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create a PyPI account at https://pypi.org/account/register/

3. Create an API token at https://pypi.org/manage/account/token/
   - Set scope to "Entire account" or specific to this project
   - Save the token securely (you'll only see it once)

## Building the Package

Build the package distribution files:

```bash
uv build
```

This creates:
- `dist/apollo_io_mcp_server-0.1.0.tar.gz` (source distribution)
- `dist/apollo_io_mcp_server-0.1.0-py3-none-any.whl` (wheel)

## Publishing to PyPI

### Option 1: Using `uv publish` (Recommended)

```bash
# Set your PyPI token
export UV_PUBLISH_TOKEN="pypi-your-token-here"

# Publish to PyPI
uv publish
```

### Option 2: Using `twine`

If you prefer to use twine:

```bash
# Install twine
uv pip install twine

# Upload to PyPI
twine upload dist/*
```

When prompted, enter:
- Username: `__token__`
- Password: Your PyPI API token (including the `pypi-` prefix)

## Test Publishing (Recommended First Step)

Before publishing to the main PyPI, test with TestPyPI:

```bash
# Build the package
uv build

# Publish to TestPyPI
export UV_PUBLISH_TOKEN="your-testpypi-token"
uv publish --publish-url https://test.pypi.org/legacy/

# Test installation from TestPyPI
uvx --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ apollo-io-mcp-server
```

## After Publishing

Once published to PyPI, users can install via:

```bash
# Install via uvx (recommended for MCP servers)
uvx apollo-io-mcp-server

# Or install via pip
pip install apollo-io-mcp-server
```

## Versioning

When making updates:

1. Update version in `pyproject.toml`
2. Follow semantic versioning (MAJOR.MINOR.PATCH)
3. Create a git tag for the release
4. Build and publish the new version

```bash
# Update version in pyproject.toml
# Then:
git tag v0.1.1
git push origin v0.1.1
uv build
uv publish
```

## Troubleshooting

### Build Errors

If you encounter build errors:
- Ensure all dependencies are listed in `pyproject.toml`
- Check that `apollo/` directory exists and has `__init__.py`
- Verify `server.py` and `apollo_client.py` are at the root

### Upload Errors

If upload fails:
- Verify your API token is correct
- Ensure the version doesn't already exist on PyPI
- Check that all required metadata is present in `pyproject.toml`

### Installation Issues

If users report installation issues:
- Test installation in a clean environment
- Verify all dependencies are correctly specified
- Check that entry point is configured correctly

## Resources

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Semantic Versioning](https://semver.org/)
