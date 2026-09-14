#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Contract tests for the default lint hook on provider component bases."""

from typing import Any

import pytest

from pyvider.actions.base import BaseAction
from pyvider.data_sources.base import BaseDataSource
from pyvider.ephemerals.base import BaseEphemeralResource
from pyvider.lint import LintContext, LintSelector
from pyvider.list_resources.base import BaseListResource
from pyvider.providers.base import BaseProvider
from pyvider.resources.base import BaseResource
from pyvider.state_stores.base import BaseStateStore


@pytest.mark.parametrize(
    "base_class",
    [
        pytest.param(BaseProvider, id="provider"),
        pytest.param(BaseResource, id="resource"),
        pytest.param(BaseDataSource, id="data-source"),
        pytest.param(BaseEphemeralResource, id="ephemeral-resource"),
        pytest.param(BaseListResource, id="list-resource"),
        pytest.param(BaseAction, id="action"),
        pytest.param(BaseStateStore, id="state-store"),
    ],
)
async def test_default_lint_hook_returns_no_findings(base_class: type[Any]) -> None:
    ctx = LintContext(config=object(), selector=LintSelector(include={"all"}))

    assert await base_class.lint(object(), ctx) == ()
