# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Documentation snippet validation tests.

These tests ensure all code snippets in the documentation are syntactically valid Python.
This prevents broken examples from appearing in the documentation.
"""

import ast
from pathlib import Path

import pytest


def get_all_snippet_files() -> list[Path]:
    """Get all Python snippet files from docs/snippets/."""
    snippets_dir = Path(__file__).parent.parent.parent / "docs" / "snippets"
    if not snippets_dir.exists():
        pytest.skip(f"Snippets directory not found: {snippets_dir}")

    snippet_files = list(snippets_dir.rglob("*.py"))
    if not snippet_files:
        pytest.skip("No snippet files found")

    return snippet_files


@pytest.mark.parametrize("snippet_file", get_all_snippet_files())
def test_snippet_valid_python(snippet_file: Path) -> None:
    """Ensure snippet is syntactically valid Python."""
    code = snippet_file.read_text()

    try:
        ast.parse(code)
    except SyntaxError as e:
        pytest.fail(
            f"Syntax error in {snippet_file.relative_to(Path.cwd())}:\nLine {e.lineno}: {e.msg}\n{e.text}"
        )


@pytest.mark.parametrize("snippet_file", get_all_snippet_files())
def test_snippet_has_docstring(snippet_file: Path) -> None:
    """Ensure snippet has a module-level docstring explaining its purpose."""
    code = snippet_file.read_text()
    tree = ast.parse(code)

    # Get module docstring
    docstring = ast.get_docstring(tree)

    if not docstring:
        pytest.fail(
            f"Missing docstring in {snippet_file.relative_to(Path.cwd())}.\n"
            "All snippets should have a module docstring explaining their purpose "
            "and where they are used."
        )

    # Check that docstring mentions usage
    if "Used in:" not in docstring:
        pytest.fail(
            f"Docstring in {snippet_file.relative_to(Path.cwd())} should include "
            "'Used in:' section explaining where the snippet is used."
        )


@pytest.mark.parametrize("snippet_file", get_all_snippet_files())
def test_snippet_imports_are_valid(snippet_file: Path) -> None:
    """Check that snippet imports look reasonable (basic sanity check)."""
    code = snippet_file.read_text()
    tree = ast.parse(code)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    # Ensure snippets import from pyvider (this is a pyvider doc after all)
    pyvider_imports = [imp for imp in imports if imp.startswith("pyvider")]

    # Skip check for schema/pattern snippets that might just show patterns
    if "patterns" in str(snippet_file) or "schema" in str(snippet_file):
        # These might not import pyvider directly
        return

    if not pyvider_imports:
        pytest.fail(
            f"Snippet {snippet_file.relative_to(Path.cwd())} doesn't import "
            "from pyvider. Documentation snippets should demonstrate pyvider usage."
        )


def test_all_snippet_categories_exist() -> None:
    """Ensure all expected snippet categories exist."""
    snippets_dir = Path(__file__).parent.parent.parent / "docs" / "snippets"

    if not snippets_dir.exists():
        pytest.skip("Snippets directory not found")

    expected_categories = {
        "resources": "Resource implementation examples",
        "data_sources": "Data source implementation examples",
        "schema": "Schema type examples",
        "patterns": "Common implementation patterns",
    }

    for category, description in expected_categories.items():
        category_dir = snippets_dir / category
        assert category_dir.exists(), f"Missing snippet category: {category} ({description})"
        assert category_dir.is_dir(), f"{category} should be a directory"


def test_snippet_file_naming_convention() -> None:
    """Ensure snippet files follow naming conventions (lowercase with underscores)."""
    snippet_files = get_all_snippet_files()

    for snippet_file in snippet_files:
        filename = snippet_file.name

        # Should be .py files
        assert filename.endswith(".py"), f"Snippet should be .py file: {filename}"

        # Should be lowercase with underscores (snake_case)
        name_without_ext = filename[:-3]  # Remove .py
        assert name_without_ext.islower() or "_" in name_without_ext, (
            f"Snippet filename should use snake_case: {filename}"
        )

        # Shouldn't have spaces
        assert " " not in filename, f"Snippet filename shouldn't have spaces: {filename}"


if __name__ == "__main__":
    # Allow running tests directly for quick validation
    pytest.main([__file__, "-v"])
