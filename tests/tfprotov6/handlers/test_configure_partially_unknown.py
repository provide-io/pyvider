#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A provider block with an unknown value in it defers, it does not fail.

Terraform sends the provider configuration as it stands during the plan and
apply walks, and only the import walk requires it to be wholly known
(internal/terraform/node_provider.go:148-156). So the ordinary shape is an
object that is itself known with an unknown somewhere inside it:

    provider "x" {
      token = aws_secretsmanager_secret_version.t.secret_string
    }

on the run that creates that secret version.

The handler guarded on `config_cty.is_unknown`, which is true only when the
*whole* object is unknown -- something Terraform does not send. The realistic
case fell through to `config_to_attrs_instance`, which returns None for a value
that is not wholly known so that a provider is never handed a half-known object,
and that None was turned into a hard `ProviderConfigurationError`. The plan
failed, while the log line right above it said "deferring configuration".
"""

from __future__ import annotations

from typing import Any, ClassVar

import attrs
import pytest

from pyvider.conversion import marshal
from pyvider.cty import CtyString, CtyValue
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.configure_provider import ConfigureProviderHandler
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.schema import a_str, s_provider


@attrs.define(frozen=True)
class ProviderConfig:
    token: str | None = None
    region: str | None = None


class ConfigurableProvider(BaseProvider):
    configured_with: ClassVar[list[Any]] = []

    @classmethod
    def get_schema(cls) -> Any:
        return s_provider(
            {
                "token": a_str(required=True),
                "region": a_str(),
            }
        )

    async def configure(self, config: Any) -> None:
        type(self).configured_with.append(config)


@pytest.fixture
def provider() -> Any:
    ConfigurableProvider.configured_with = []
    previous = hub.get_component("singleton", "provider")
    instance = ConfigurableProvider(metadata=ProviderMetadata(name="t", version="0"))
    # `schema` is a read-only property fed by setup(); the private field is
    # what setup() fills in, and this test does not need the rest of setup.
    instance._final_schema = ConfigurableProvider.get_schema()
    # `config_class` is an attrs field that setup() fills in from the schema.
    instance.config_class = ProviderConfig
    hub.register("singleton", "provider", instance)

    yield ConfigurableProvider

    if previous is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous)
    ConfigurableProvider.configured_with = []


@pytest.mark.asyncio
async def test_a_partially_unknown_provider_config_does_not_fail(provider: Any) -> None:
    """The realistic case: one attribute is not computable yet."""
    block = ConfigurableProvider.get_schema().block
    config = marshal(
        block.to_cty_type().validate({"token": CtyValue.unknown(CtyString()), "region": "eu-west-1"}),
        schema=block,
    )

    response = await ConfigureProviderHandler(
        pb.ConfigureProvider.Request(terraform_version="1.17.0", config=config),
        context=None,
    )

    assert not response.diagnostics, (
        "a provider block carrying an unknown value failed configuration; "
        f"Terraform sends these during plan: {response.diagnostics}"
    )


@pytest.mark.asyncio
async def test_a_wholly_known_config_still_configures(provider: Any) -> None:
    """The deferral must not swallow a configuration that is ready."""
    block = ConfigurableProvider.get_schema().block
    config = marshal({"token": "abc", "region": "eu-west-1"}, schema=block)

    response = await ConfigureProviderHandler(
        pb.ConfigureProvider.Request(terraform_version="1.17.0", config=config),
        context=None,
    )

    assert not response.diagnostics, f"configure failed: {response.diagnostics}"
    assert provider.configured_with, "the provider's configure hook never ran"
    assert provider.configured_with[0].token == "abc"


@pytest.mark.asyncio
async def test_the_configure_hook_is_not_run_with_a_half_known_config(provider: Any) -> None:
    """Deferring means the provider is not handed values it cannot use."""
    block = ConfigurableProvider.get_schema().block
    config = marshal(
        block.to_cty_type().validate({"token": CtyValue.unknown(CtyString()), "region": "eu-west-1"}),
        schema=block,
    )

    await ConfigureProviderHandler(
        pb.ConfigureProvider.Request(terraform_version="1.17.0", config=config),
        context=None,
    )

    assert provider.configured_with == [], "the provider was configured from a half-known object"


# 🐍🏗️🔚
