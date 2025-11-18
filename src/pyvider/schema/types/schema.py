#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from attrs import define, field
from provide.foundation import logger

from pyvider.cty import CtyValidationError

# CORRECTED IMPORT: Replace the obsolete PvsBlock with the new PvsObjectType.
from pyvider.schema.types.object import PvsObjectType


@define(frozen=True, kw_only=True)
class PvsSchema:
    """
    Represents a complete schema definition for a provider, resource, or data source.
    This class is the root of a schema tree.

    Attributes:
        version: An integer representing the schema version, used for state upgrades.
        block: The root block of the schema, defining its attributes and nested blocks.
    """

    version: int = field(validator=lambda i, a, v: v > 0)
    block: PvsObjectType = field()

    def validate_config(self, config: Any) -> None:
        """
        Validates a configuration against this schema by converting the schema
        to its CtyType representation and invoking its validation logic.

        This method raises CtyValidationError on failure, which is the
        expected contract for direct validation. Higher-level handlers are
        responsible for catching this exception and creating diagnostics.
        """
        logger.debug("Validating configuration against schema", schema_version=self.version)
        if not isinstance(config, dict):
            raise CtyValidationError(f"Configuration must be a dictionary, but got {type(config).__name__}.")

        # Convert the schema's block to its CtyType representation to get the validator.
        validator = self.block.to_cty_type()

        # The CtyType's validate method will raise CtyValidationError on failure.
        validator.validate(config)

    def to_cty_type(self) -> PvsObjectType:
        """
        Returns the CtyType representation of the schema's root block.
        Since the block is now a PvsObjectType, this is a direct return.
        """
        return self.block


# 🐍🏗️🔚
