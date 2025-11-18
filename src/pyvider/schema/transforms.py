#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import attrs
from provide.foundation import logger

from pyvider.schema.types.attribute import PvsAttribute
from pyvider.schema.types.object import PvsObjectType
from pyvider.schema.types.schema import PvsSchema


class PvsSchemaTransformer:
    """Utility for transforming and extending Terraform schemas."""

    def add_attribute(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            logger.error(
                "Attempted to add duplicate attribute to schema",
                operation="add_attribute",
                attribute_name=attribute.name,
                existing_attributes=list(block.attributes.keys()),
            )
            raise ValueError(
                f"Cannot add attribute '{attribute.name}' to schema: attribute already exists.\n\n"
                f"Suggestion: Use a unique attribute name or remove the existing attribute first.\n"
                f"Existing attributes: {', '.join(block.attributes.keys())}"
            )

        logger.debug(
            "Adding attribute to schema",
            operation="add_attribute",
            attribute_name=attribute.name,
            attribute_type=type(attribute.type).__name__,
            required=attribute.required,
            optional=attribute.optional,
            computed=attribute.computed,
        )

        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def remove_attribute(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            logger.error(
                "Attempted to remove non-existent attribute from schema",
                operation="remove_attribute",
                attribute_name=attribute_name,
                available_attributes=list(block.attributes.keys()),
            )
            raise ValueError(
                f"Cannot remove attribute '{attribute_name}' from schema: attribute not found.\n\n"
                f"Suggestion: Check the attribute name for typos.\n"
                f"Available attributes: {', '.join(block.attributes.keys())}"
            )

        logger.debug(
            "Removing attribute from schema",
            operation="remove_attribute",
            attribute_name=attribute_name,
        )

        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def merge_schemas(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        logger.debug(
            "Starting schema merge operation",
            operation="merge_schemas",
            schema_count=len(schemas),
        )

        all_attrs = {}
        all_block_types = []
        block_type_names = set()

        for idx, s in enumerate(schemas):
            block = s.block
            for name, attr in block.attributes.items():
                if name in all_attrs:
                    logger.error(
                        "Attribute name conflict during schema merge",
                        operation="merge_schemas",
                        conflicting_attribute=name,
                        schema_index=idx,
                        total_schemas=len(schemas),
                    )
                    raise ValueError(
                        f"Cannot merge schemas: attribute name conflict for '{name}'.\n\n"
                        f"Suggestion: Rename one of the conflicting attributes to have a unique name.\n"
                        f"Conflict detected at schema index {idx} of {len(schemas)} schemas being merged."
                    )
                all_attrs[name] = attr

            for bt in block.block_types:
                if bt.type_name in block_type_names:
                    logger.error(
                        "Block type name conflict during schema merge",
                        operation="merge_schemas",
                        conflicting_block_type=bt.type_name,
                        schema_index=idx,
                        total_schemas=len(schemas),
                    )
                    raise ValueError(
                        f"Cannot merge schemas: block type name conflict for '{bt.type_name}'.\n\n"
                        f"Suggestion: Rename one of the conflicting block types to have a unique name.\n"
                        f"Conflict detected at schema index {idx} of {len(schemas)} schemas being merged."
                    )
                all_block_types.append(bt)
                block_type_names.add(bt.type_name)

        logger.info(
            "Schema merge completed successfully",
            operation="merge_schemas",
            total_attributes=len(all_attrs),
            total_block_types=len(all_block_types),
            source_schema_count=len(schemas),
        )

        new_block = PvsObjectType(
            attributes=all_attrs,
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)


# 🐍🏗️🔚
