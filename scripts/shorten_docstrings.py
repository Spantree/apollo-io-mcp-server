#!/usr/bin/env python3
"""
Script to shorten tool docstrings to reduce MCP token usage.

This script:
1. Backs up original files
2. Extracts concise docstrings (Args, Returns, one-line description)
3. Replaces verbose docstrings with minimal versions
4. References external docs for details

Usage:
    python scripts/shorten_docstrings.py [--dry-run]
"""

import re
import sys
from pathlib import Path
from datetime import datetime

# Mapping of verbose sections to keep
SECTIONS_TO_KEEP = ['Args:', 'Returns:', 'Yields:', 'Raises:', 'Note:']

def extract_concise_docstring(full_docstring, tool_name, module_name):
    """
    Extract a concise version of a docstring.

    Keeps:
    - First line (one-line summary)
    - Args/Returns sections
    - Master API key note if present

    Removes:
    - Long explanations
    - Use cases
    - Workflows
    - Examples
    - Detailed field descriptions
    """
    lines = full_docstring.split('\n')

    # Get first meaningful line as summary
    summary = None
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(('"""', "'''")):
            summary = stripped
            break

    if not summary:
        summary = f"{tool_name.replace('_', ' ').title()}"

    # Check for master API key requirement
    needs_master_key = 'master API key' in full_docstring.lower() or 'REQUIRES MASTER' in full_docstring

    # Extract Args section
    args_section = extract_section(full_docstring, 'Args:', ['Returns:', 'Yields:', 'Raises:', 'Note:', 'PARAMETERS:', 'USE CASES:'])

    # Extract Returns section
    returns_section = extract_section(full_docstring, 'Returns:', ['Args:', 'Yields:', 'Raises:', 'Note:', 'RETURNED DATA:', 'USE CASES:'])
    if not returns_section:
        returns_section = extract_section(full_docstring, 'RETURNED DATA:', ['Args:', 'USE CASES:', 'WORKFLOW:'])

    # Build concise docstring
    parts = [summary]

    if needs_master_key:
        parts.append("Master API key required.")

    parts.append(f"\nSee docs/tools/{module_name}.md for detailed documentation and examples.")

    if args_section:
        parts.append(f"\n{args_section}")

    if returns_section:
        # Simplify returns section
        if len(returns_section) > 200:
            # Just keep structure info
            returns_section = returns_section[:200] + "..."
        parts.append(f"\n{returns_section}")

    return '\n'.join(parts)


def extract_section(docstring, section_name, stop_at_sections):
    """Extract a specific section from docstring."""
    lines = docstring.split('\n')
    in_section = False
    section_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith(section_name):
            in_section = True
            section_lines.append(section_name)
            continue

        if in_section:
            # Stop at next major section
            if any(stripped.startswith(s) for s in stop_at_sections):
                break
            section_lines.append(line)

    if section_lines:
        return '\n'.join(section_lines).strip()
    return None


def shorten_tool_file(file_path, dry_run=False):
    """Shorten all docstrings in a tool file."""
    module_name = file_path.stem  # e.g., 'accounts' from 'accounts.py'

    with open(file_path, 'r') as f:
        content = f.read()

    # Find all async def functions with docstrings
    pattern = r'(    @mcp\.tool\(\)\n    async def (\w+)\([^)]*\)[^:]*:\n        """)(.*?)(""")'

    def replace_docstring(match):
        prefix = match.group(1)
        tool_name = match.group(2)
        old_docstring = match.group(3)
        suffix = match.group(4)

        # Generate concise version
        new_docstring = extract_concise_docstring(old_docstring, tool_name, module_name)

        print(f"  {tool_name}: {len(old_docstring)} → {len(new_docstring)} chars (-{len(old_docstring)-len(new_docstring)})")

        return f"{prefix}{new_docstring}{suffix}"

    new_content = re.sub(pattern, replace_docstring, content, flags=re.DOTALL)

    if dry_run:
        print(f"[DRY RUN] Would update {file_path}")
        return False

    # Backup original
    backup_path = file_path.with_suffix('.py.backup')
    with open(backup_path, 'w') as f:
        f.write(content)
    print(f"  Backed up to {backup_path}")

    # Write shortened version
    with open(file_path, 'w') as f:
        f.write(new_content)

    return True


def main():
    dry_run = '--dry-run' in sys.argv

    print("Shortening tool docstrings...")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")

    tools_dir = Path('tools')
    tool_files = [
        tools_dir / 'people.py',
        tools_dir / 'organizations.py',
        tools_dir / 'contacts.py',
        tools_dir / 'accounts.py',
        tools_dir / 'misc.py',
    ]

    for tool_file in tool_files:
        if not tool_file.exists():
            print(f"⚠ Skipping {tool_file} (not found)")
            continue

        print(f"\n{tool_file.name}:")
        shorten_tool_file(tool_file, dry_run)

    print("\n✓ Done!")
    if not dry_run:
        print("\nOriginal files backed up with .py.backup extension")
        print("Detailed documentation available in docs/tools/*.md")


if __name__ == '__main__':
    main()
