import time
from typing import Any

import msgpack
from provide.foundation.errors import resilient

from pyvider.common.encryption import decrypt
from pyvider.conversion import marshal, unmarshal
from pyvider.exceptions import PyviderError, ResourceError
from pyvider.hub import hub
from pyvider.observability import (
    handler_duration,
    handler_errors,
    handler_requests,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


@resilient()
async def ReadResourceHandler(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Handle read resource request."""
    start_time = time.perf_counter()
    handler_requests.inc(handler="ReadResource")

    try:
        return await _read_resource_impl(request, context)
    except Exception:
        handler_errors.inc(handler="ReadResource")
        raise
    finally:
        duration = time.perf_counter() - start_time
        handler_duration.observe(duration, handler="ReadResource")


async def x__read_resource_impl__mutmut_orig(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_1(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = None
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_2(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = ""
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_3(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = None
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_4(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component(None, request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_5(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", None)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_6(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component(request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_7(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", )
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_8(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("XXresourceXX", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_9(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("RESOURCE", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_10(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_11(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(None)

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_12(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = None
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_13(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component(None, "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_14(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", None)
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_15(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_16(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", )
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_17(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("XXsingletonXX", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_18(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("SINGLETON", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_19(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "XXproviderXX")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_20(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "PROVIDER")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_21(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_22(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError(None)

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_23(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("XXProvider instance not found in hub.XX")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_24(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("provider instance not found in hub.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_25(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("PROVIDER INSTANCE NOT FOUND IN HUB.")

        resource_schema = resource_class.get_schema()
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_26(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
    response = pb.ReadResource.Response()
    resource_context = None
    try:
        resource_class = hub.get_component("resource", request.type_name)
        if not resource_class:
            raise ValueError(f"Resource type '{request.type_name}' not registered")

        provider_instance = hub.get_component("singleton", "provider")
        if not provider_instance:
            raise RuntimeError("Provider instance not found in hub.")

        resource_schema = None
        prior_state_cty = unmarshal(request.current_state, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_27(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_cty = None
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_28(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_cty = unmarshal(None, schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_29(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_cty = unmarshal(request.current_state, schema=None)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_30(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_cty = unmarshal(schema=resource_schema.block)
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_31(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_cty = unmarshal(request.current_state, )
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_32(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = None

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_33(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(None, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_34(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, None)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_35(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_36(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, )

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_37(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = ""
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_38(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class or request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_39(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class") or resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_40(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(None, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_41(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, None)
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_42(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr("private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_43(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, )
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_44(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "XXprivate_state_classXX")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_45(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "PRIVATE_STATE_CLASS")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_46(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = None
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_47(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(None)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_48(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = None
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_49(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(None, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_50(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=None)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_51(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_52(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, )
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_53(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=True)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_54(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = None
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_55(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(None) from e

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


async def x__read_resource_impl__mutmut_56(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = None
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


async def x__read_resource_impl__mutmut_57(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = None
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


async def x__read_resource_impl__mutmut_58(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=None,
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


async def x__read_resource_impl__mutmut_59(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=None,
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


async def x__read_resource_impl__mutmut_60(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=None,
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


async def x__read_resource_impl__mutmut_61(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
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


async def x__read_resource_impl__mutmut_62(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
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


async def x__read_resource_impl__mutmut_63(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
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


async def x__read_resource_impl__mutmut_64(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
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


async def x__read_resource_impl__mutmut_65(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=provider_instance.metadata.capabilities,
        )
        new_state_attrs = None

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


async def x__read_resource_impl__mutmut_66(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=provider_instance.metadata.capabilities,
        )
        new_state_attrs = await resource_handler.read(None)

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


async def x__read_resource_impl__mutmut_67(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=provider_instance.metadata.capabilities,
        )
        new_state_attrs = await resource_handler.read(resource_context)

        if new_state_attrs is None:
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


async def x__read_resource_impl__mutmut_68(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=provider_instance.metadata.capabilities,
        )
        new_state_attrs = await resource_handler.read(resource_context)

        if new_state_attrs is not None:
            raw_state_dict = None
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


async def x__read_resource_impl__mutmut_69(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

        resource_handler = resource_class()
        resource_context = ResourceContext(
            config=None,
            state=prior_state_instance,
            private_state=private_state_instance,
            capabilities=provider_instance.metadata.capabilities,
        )
        new_state_attrs = await resource_handler.read(resource_context)

        if new_state_attrs is not None:
            raw_state_dict = attrs_to_dict_for_cty(None)
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


async def x__read_resource_impl__mutmut_70(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            validator_type = None
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


async def x__read_resource_impl__mutmut_71(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            new_state_cty = None
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


async def x__read_resource_impl__mutmut_72(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            new_state_cty = validator_type.validate(None)
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


async def x__read_resource_impl__mutmut_73(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            marshalled_new_state = None
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


async def x__read_resource_impl__mutmut_74(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            marshalled_new_state = marshal(None, schema=resource_schema.block)
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


async def x__read_resource_impl__mutmut_75(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            marshalled_new_state = marshal(new_state_cty, schema=None)
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


async def x__read_resource_impl__mutmut_76(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            marshalled_new_state = marshal(schema=resource_schema.block)
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


async def x__read_resource_impl__mutmut_77(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            marshalled_new_state = marshal(new_state_cty, )
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


async def x__read_resource_impl__mutmut_78(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            response.new_state.msgpack = None
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


async def x__read_resource_impl__mutmut_79(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            response.new_state.msgpack = None

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


async def x__read_resource_impl__mutmut_80(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            response.new_state.msgpack = b"XX\xc0XX"

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


async def x__read_resource_impl__mutmut_81(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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


async def x__read_resource_impl__mutmut_82(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
            response.new_state.msgpack = b"\xC0"

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


async def x__read_resource_impl__mutmut_83(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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

        response.private = None

    except PyviderError as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_84(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
        diag = None
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_85(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_86(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
        response.diagnostics.append(None)
    except Exception as e:
        diag = await create_diagnostic_from_exception(e)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_87(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
        diag = None
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_88(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
        diag = await create_diagnostic_from_exception(None)
        response.diagnostics.append(diag)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_89(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
        response.diagnostics.append(None)

    if resource_context and resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_90(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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

    if resource_context or resource_context.diagnostics:
        response.diagnostics.extend(resource_context.diagnostics)

    return response


async def x__read_resource_impl__mutmut_91(request: pb.ReadResource.Request, context: Any) -> pb.ReadResource.Response:
    """Implementation of ReadResource handler."""
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
        prior_state_instance = cty_to_attrs_instance(prior_state_cty, resource_class.state_class)

        private_state_instance = None
        if (
            hasattr(resource_class, "private_state_class")
            and resource_class.private_state_class
            and request.private
        ):
            try:
                decrypted_bytes = decrypt(request.private)
                private_data = msgpack.unpackb(decrypted_bytes, raw=False)
                private_state_instance = resource_class.private_state_class(**private_data)
            except Exception as e:
                raise ResourceError(f"Failed to deserialize private state for {request.type_name}.") from e

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
        response.diagnostics.extend(None)

    return response

x__read_resource_impl__mutmut_mutants : ClassVar[MutantDict] = {
'x__read_resource_impl__mutmut_1': x__read_resource_impl__mutmut_1, 
    'x__read_resource_impl__mutmut_2': x__read_resource_impl__mutmut_2, 
    'x__read_resource_impl__mutmut_3': x__read_resource_impl__mutmut_3, 
    'x__read_resource_impl__mutmut_4': x__read_resource_impl__mutmut_4, 
    'x__read_resource_impl__mutmut_5': x__read_resource_impl__mutmut_5, 
    'x__read_resource_impl__mutmut_6': x__read_resource_impl__mutmut_6, 
    'x__read_resource_impl__mutmut_7': x__read_resource_impl__mutmut_7, 
    'x__read_resource_impl__mutmut_8': x__read_resource_impl__mutmut_8, 
    'x__read_resource_impl__mutmut_9': x__read_resource_impl__mutmut_9, 
    'x__read_resource_impl__mutmut_10': x__read_resource_impl__mutmut_10, 
    'x__read_resource_impl__mutmut_11': x__read_resource_impl__mutmut_11, 
    'x__read_resource_impl__mutmut_12': x__read_resource_impl__mutmut_12, 
    'x__read_resource_impl__mutmut_13': x__read_resource_impl__mutmut_13, 
    'x__read_resource_impl__mutmut_14': x__read_resource_impl__mutmut_14, 
    'x__read_resource_impl__mutmut_15': x__read_resource_impl__mutmut_15, 
    'x__read_resource_impl__mutmut_16': x__read_resource_impl__mutmut_16, 
    'x__read_resource_impl__mutmut_17': x__read_resource_impl__mutmut_17, 
    'x__read_resource_impl__mutmut_18': x__read_resource_impl__mutmut_18, 
    'x__read_resource_impl__mutmut_19': x__read_resource_impl__mutmut_19, 
    'x__read_resource_impl__mutmut_20': x__read_resource_impl__mutmut_20, 
    'x__read_resource_impl__mutmut_21': x__read_resource_impl__mutmut_21, 
    'x__read_resource_impl__mutmut_22': x__read_resource_impl__mutmut_22, 
    'x__read_resource_impl__mutmut_23': x__read_resource_impl__mutmut_23, 
    'x__read_resource_impl__mutmut_24': x__read_resource_impl__mutmut_24, 
    'x__read_resource_impl__mutmut_25': x__read_resource_impl__mutmut_25, 
    'x__read_resource_impl__mutmut_26': x__read_resource_impl__mutmut_26, 
    'x__read_resource_impl__mutmut_27': x__read_resource_impl__mutmut_27, 
    'x__read_resource_impl__mutmut_28': x__read_resource_impl__mutmut_28, 
    'x__read_resource_impl__mutmut_29': x__read_resource_impl__mutmut_29, 
    'x__read_resource_impl__mutmut_30': x__read_resource_impl__mutmut_30, 
    'x__read_resource_impl__mutmut_31': x__read_resource_impl__mutmut_31, 
    'x__read_resource_impl__mutmut_32': x__read_resource_impl__mutmut_32, 
    'x__read_resource_impl__mutmut_33': x__read_resource_impl__mutmut_33, 
    'x__read_resource_impl__mutmut_34': x__read_resource_impl__mutmut_34, 
    'x__read_resource_impl__mutmut_35': x__read_resource_impl__mutmut_35, 
    'x__read_resource_impl__mutmut_36': x__read_resource_impl__mutmut_36, 
    'x__read_resource_impl__mutmut_37': x__read_resource_impl__mutmut_37, 
    'x__read_resource_impl__mutmut_38': x__read_resource_impl__mutmut_38, 
    'x__read_resource_impl__mutmut_39': x__read_resource_impl__mutmut_39, 
    'x__read_resource_impl__mutmut_40': x__read_resource_impl__mutmut_40, 
    'x__read_resource_impl__mutmut_41': x__read_resource_impl__mutmut_41, 
    'x__read_resource_impl__mutmut_42': x__read_resource_impl__mutmut_42, 
    'x__read_resource_impl__mutmut_43': x__read_resource_impl__mutmut_43, 
    'x__read_resource_impl__mutmut_44': x__read_resource_impl__mutmut_44, 
    'x__read_resource_impl__mutmut_45': x__read_resource_impl__mutmut_45, 
    'x__read_resource_impl__mutmut_46': x__read_resource_impl__mutmut_46, 
    'x__read_resource_impl__mutmut_47': x__read_resource_impl__mutmut_47, 
    'x__read_resource_impl__mutmut_48': x__read_resource_impl__mutmut_48, 
    'x__read_resource_impl__mutmut_49': x__read_resource_impl__mutmut_49, 
    'x__read_resource_impl__mutmut_50': x__read_resource_impl__mutmut_50, 
    'x__read_resource_impl__mutmut_51': x__read_resource_impl__mutmut_51, 
    'x__read_resource_impl__mutmut_52': x__read_resource_impl__mutmut_52, 
    'x__read_resource_impl__mutmut_53': x__read_resource_impl__mutmut_53, 
    'x__read_resource_impl__mutmut_54': x__read_resource_impl__mutmut_54, 
    'x__read_resource_impl__mutmut_55': x__read_resource_impl__mutmut_55, 
    'x__read_resource_impl__mutmut_56': x__read_resource_impl__mutmut_56, 
    'x__read_resource_impl__mutmut_57': x__read_resource_impl__mutmut_57, 
    'x__read_resource_impl__mutmut_58': x__read_resource_impl__mutmut_58, 
    'x__read_resource_impl__mutmut_59': x__read_resource_impl__mutmut_59, 
    'x__read_resource_impl__mutmut_60': x__read_resource_impl__mutmut_60, 
    'x__read_resource_impl__mutmut_61': x__read_resource_impl__mutmut_61, 
    'x__read_resource_impl__mutmut_62': x__read_resource_impl__mutmut_62, 
    'x__read_resource_impl__mutmut_63': x__read_resource_impl__mutmut_63, 
    'x__read_resource_impl__mutmut_64': x__read_resource_impl__mutmut_64, 
    'x__read_resource_impl__mutmut_65': x__read_resource_impl__mutmut_65, 
    'x__read_resource_impl__mutmut_66': x__read_resource_impl__mutmut_66, 
    'x__read_resource_impl__mutmut_67': x__read_resource_impl__mutmut_67, 
    'x__read_resource_impl__mutmut_68': x__read_resource_impl__mutmut_68, 
    'x__read_resource_impl__mutmut_69': x__read_resource_impl__mutmut_69, 
    'x__read_resource_impl__mutmut_70': x__read_resource_impl__mutmut_70, 
    'x__read_resource_impl__mutmut_71': x__read_resource_impl__mutmut_71, 
    'x__read_resource_impl__mutmut_72': x__read_resource_impl__mutmut_72, 
    'x__read_resource_impl__mutmut_73': x__read_resource_impl__mutmut_73, 
    'x__read_resource_impl__mutmut_74': x__read_resource_impl__mutmut_74, 
    'x__read_resource_impl__mutmut_75': x__read_resource_impl__mutmut_75, 
    'x__read_resource_impl__mutmut_76': x__read_resource_impl__mutmut_76, 
    'x__read_resource_impl__mutmut_77': x__read_resource_impl__mutmut_77, 
    'x__read_resource_impl__mutmut_78': x__read_resource_impl__mutmut_78, 
    'x__read_resource_impl__mutmut_79': x__read_resource_impl__mutmut_79, 
    'x__read_resource_impl__mutmut_80': x__read_resource_impl__mutmut_80, 
    'x__read_resource_impl__mutmut_81': x__read_resource_impl__mutmut_81, 
    'x__read_resource_impl__mutmut_82': x__read_resource_impl__mutmut_82, 
    'x__read_resource_impl__mutmut_83': x__read_resource_impl__mutmut_83, 
    'x__read_resource_impl__mutmut_84': x__read_resource_impl__mutmut_84, 
    'x__read_resource_impl__mutmut_85': x__read_resource_impl__mutmut_85, 
    'x__read_resource_impl__mutmut_86': x__read_resource_impl__mutmut_86, 
    'x__read_resource_impl__mutmut_87': x__read_resource_impl__mutmut_87, 
    'x__read_resource_impl__mutmut_88': x__read_resource_impl__mutmut_88, 
    'x__read_resource_impl__mutmut_89': x__read_resource_impl__mutmut_89, 
    'x__read_resource_impl__mutmut_90': x__read_resource_impl__mutmut_90, 
    'x__read_resource_impl__mutmut_91': x__read_resource_impl__mutmut_91
}

def _read_resource_impl(*args, **kwargs):
    result = _mutmut_trampoline(x__read_resource_impl__mutmut_orig, x__read_resource_impl__mutmut_mutants, args, kwargs)
    return result 

_read_resource_impl.__signature__ = _mutmut_signature(x__read_resource_impl__mutmut_orig)
x__read_resource_impl__mutmut_orig.__name__ = 'x__read_resource_impl'
