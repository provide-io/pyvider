#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The doc link checker must agree with the renderer that makes the anchors.

`scripts/check_doc_links.py` fails CI on anchors it believes are broken, so a
slug it computes differently from Python-Markdown's toc extension does not
merely miss a bad link -- it reports a correct one as broken, and there is no
way to satisfy it except by writing a link that does not work."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_doc_links.py"


def _load_slugify():
    """Import slugify from the script, which is not an installed module."""
    spec = importlib.util.spec_from_file_location("check_doc_links", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_doc_links"] = module
    spec.loader.exec_module(module)
    return module.slugify


slugify = _load_slugify()


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        # The case that failed a pull request: `\w` includes the underscore, so
        # toc keeps it and the anchor is `require_replace`, not `requirereplace`.
        ("`require_replace()`", "require_replace"),
        ("`_update()`", "_update"),
        ("Forcing Replacement (`requires_replace`)", "forcing-replacement-requires_replace"),
        # Backticks and asterisks are delimiters and disappear when rendered.
        ("`a_str()`", "a_str"),
        ("**Bold Heading**", "bold-heading"),
        # Ordinary prose is unaffected.
        ("Required Methods", "required-methods"),
        ("Type Signatures", "type-signatures"),
    ],
)
def test_slugify_matches_the_rendered_anchor(heading: str, expected: str) -> None:
    assert slugify(heading) == expected


def test_underscores_survive() -> None:
    """The specific regression: an identifier must not be mangled."""
    assert "_" in slugify("`private_state`")
    assert slugify("`private_state`") == "private_state"
