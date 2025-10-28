#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""This script conforms all Python files in the repository to a specific header and footer protocol."""

import ast
import os
import re
import sys

# --- Configuration ---
SHEBANG = "#!/usr/bin/env python3"
LIBRARY_HEADER = "# "
SPDX_BLOCK = """# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#"""
PLACEHOLDER_DOCSTRING = '"""TODO: Add module docstring."""'
FOOTER = "# 🐍🏗️🔚"

# Exclude files that are not part of the source code, are vendored, or are this script itself.
EXCLUDE_FILES = [
    "conform.py",
    "build_provider.py",
    "runtime-hook.py",
    "tfplugin6_pb2.py",
    "tfplugin6_pb2_grpc.py",
    ".mutmut-config.py",
]


def get_python_files():
    """Returns a list of all Python files in the current directory and subdirectories, excluding specified files."""
    files = []
    for dirpath, _, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".py") and filename not in EXCLUDE_FILES:
                files.append(os.path.join(dirpath, filename))
    return files


def get_module_docstring_and_body(content):
    """
    Extracts the module-level docstring and the rest of the code body from the file content.
    Uses AST parsing for accuracy.
    """
    try:
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree)

        if not docstring:
            return None, content.strip()

        # Find the docstring node to get its exact source and end line
        docstring_node = tree.body[0]
        end_lineno = docstring_node.end_lineno

        # The body is everything after the docstring
        body_content = "\n".join(content.splitlines()[end_lineno:])

        # Get the raw docstring with quotes to preserve formatting
        raw_docstring = ast.get_source_segment(content, docstring_node)

        return raw_docstring, body_content.strip()

    except SyntaxError:
        # Fallback for files that can't be parsed (e.g., syntax errors)
        # This is a very basic heuristic.
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith('"""') or line.strip().startswith("'''"):
                # This is likely the start of the docstring. We'll consider everything from here as the body.
                return None, "\n".join(lines[i:]).strip()
        return None, content.strip()


def conform_file(filepath) -> None:
    """Conforms a single Python file to the header/footer protocol."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
            if not content.strip():  # Skip empty or whitespace-only files
                print(f"Skipping empty file: {filepath}")
                return
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading {filepath}: {e}")
        return

    is_executable = content.startswith("#!")

    # Strip any existing shebang and leading comments to isolate the code for parsing
    lines = content.splitlines()
    code_start_index = 0
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith("#"):
            code_start_index = i
            break

    content_sans_header = "\n".join(lines[code_start_index:])

    docstring, body = get_module_docstring_and_body(content_sans_header)

    # Construct the new header
    header_parts = []
    if is_executable:
        header_parts.append(SHEBANG)
    else:
        header_parts.append(LIBRARY_HEADER)

    header_parts.append(SPDX_BLOCK)
    header_parts.append("")

    header_parts.append(docstring or PLACEHOLDER_DOCSTRING)

    new_header = "\n".join(header_parts)

    # Strip old footers and trailing whitespace from body
    body = re.sub(r"# 🐍🏗️.*", "", body).strip()

    # Construct the final content
    final_content = f"{new_header}\n\n{body}\n\n{FOOTER}\n"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Conformed: {filepath}")
    except OSError as e:
        print(f"Error writing to {filepath}: {e}")


def main() -> None:
    """Main function to find all Python files and conform them."""
    files = sys.argv[1:] if len(sys.argv) > 1 else get_python_files()

    for file in files:
        if file.endswith(".py") and os.path.basename(file) not in EXCLUDE_FILES:
            conform_file(file)


if __name__ == "__main__":
    main()

# 🐍🏗️🔚
