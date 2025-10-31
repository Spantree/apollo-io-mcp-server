#!/usr/bin/env python3
"""
Strip verbose Field descriptions from Pydantic models to reduce token usage.
These descriptions get serialized into JSON schemas sent to Claude.
"""

import re
from pathlib import Path

def strip_descriptions(content: str) -> str:
    """
    Remove description= arguments from Field() calls.
    Keep default= and other arguments.
    """
    # Pattern to match Field(..., description="...", ...)
    # This handles multi-line descriptions too
    pattern = r'Field\((.*?)\)'

    def replace_field(match):
        field_content = match.group(1)

        # Remove description parameter (handles multi-line)
        # Match: description="..." or description='...'
        field_content = re.sub(
            r',?\s*description\s*=\s*["\'].*?["\']',
            '',
            field_content,
            flags=re.DOTALL
        )

        # Clean up any trailing commas or extra whitespace
        field_content = re.sub(r',\s*\)', ')', field_content)
        field_content = re.sub(r'\(\s*,', '(', field_content)
        field_content = field_content.strip()

        # If Field now has no arguments, just use Field()
        if not field_content or field_content == '':
            return 'Field()'

        return f'Field({field_content})'

    # Apply the replacement
    result = re.sub(pattern, replace_field, content, flags=re.DOTALL)

    return result


def process_file(file_path: Path):
    """Process a single Python file to strip Field descriptions."""
    print(f"Processing {file_path}...")

    content = file_path.read_text()
    original_size = len(content)

    # Strip descriptions
    new_content = strip_descriptions(content)
    new_size = len(content)

    if original_size != new_size:
        # Write back
        file_path.write_text(new_content)
        saved = original_size - new_size
        print(f"  ✓ Saved {saved} characters")
    else:
        print(f"  - No changes needed")


def main():
    """Process all Python files in apollo/ directory."""
    apollo_dir = Path(__file__).parent.parent / "apollo"

    if not apollo_dir.exists():
        print(f"Error: {apollo_dir} not found")
        return

    python_files = list(apollo_dir.glob("*.py"))
    print(f"Found {len(python_files)} Python files in apollo/\n")

    for file_path in sorted(python_files):
        process_file(file_path)

    print("\n✓ Done! Field descriptions stripped from all files.")
    print("This should drastically reduce MCP token usage.")


if __name__ == "__main__":
    main()
