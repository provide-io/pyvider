#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from provide.foundation import logger
import pytest

from pyvider.cty import CtyMark, CtyString


@pytest.mark.xfail(reason="Requires structlog integration with a CtyValue redacting processor.")
def test_sensitive_cty_value_is_redacted_in_logs(caplog) -> None:
    """
    TDD Contract: Verifies that a CtyValue marked as sensitive
    is automatically redacted when passed to a structured logger.
    """
    # GIVEN a CtyValue marked as sensitive
    sensitive_mark = CtyMark("sensitive")
    secret_value = CtyString().validate("my-super-secret-api-key").mark(sensitive_mark)

    # WHEN it is included in a log message
    logger.info("Attempting to log sensitive data", user_token=secret_value)

    # THEN the raw log output must not contain the secret value
    log_output = caplog.text
    assert "my-super-secret-api-key" not in log_output
    assert "[SENSITIVE]" in log_output


# 🐍🏗️🔚
