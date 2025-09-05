from typing import Any

import msgpack

from provide.foundation.errors import with_error_handling
from pyvider.common.encryption import decrypt
from pyvider.conversion import marshal, unmarshal
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext

from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
)


@with_error_handling()
async def ReadResourceHandler(
    request: pb.ReadResource.Request, context: Any
) -> pb.ReadResource.Response:
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(
            prior_state_cty, resource_class.state_class
        )

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(
                    **private_data
                )
            except Exception as e:
                raise ResourceError(
                    f"Failed to deserialize private state for {request.type_name}."
                ) from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=provider_instance.metadata.capabilities,
        )
        new_state_attrs = await resource_handler.read(resource_context)

        if new_state_attrs is not None:
            raw_state_dict = attrs_to_dict_for_cty(new_state_attrs)
            validator_type = resource_schema.block.to_cty_type()
            new_state_cty = validator_type.validate(raw_state_dict)
            marshalled_new_state = marshal(new_state_cty, schema=resource_schema.block)
            response.new_state.msgpack = marshalled_new_state.msgpack
        else:
            response.new_state.msgpack = b"\xc0"

        response.private = request.private

    except PyviderError as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response
