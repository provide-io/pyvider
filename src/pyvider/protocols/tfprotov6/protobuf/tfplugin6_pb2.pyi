from collections.abc import Iterable as _Iterable, Mapping as _Mapping
import datetime
from typing import Any, ClassVar as _ClassVar

from google.protobuf import (
    descriptor as _descriptor,
    message as _message,
    timestamp_pb2 as _timestamp_pb2,
)
from google.protobuf.internal import (
    containers as _containers,
    enum_type_wrapper as _enum_type_wrapper,
)

DESCRIPTOR: _descriptor.FileDescriptor

class StringKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLAIN: _ClassVar[StringKind]
    MARKDOWN: _ClassVar[StringKind]

PLAIN: StringKind
MARKDOWN: StringKind

class DynamicValue(_message.Message):
    __slots__ = ("json", "msgpack")
    MSGPACK_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    msgpack: bytes
    json: bytes
    def __init__(self, msgpack: bytes | None = ..., json: bytes | None = ...) -> None: ...

class Diagnostic(_message.Message):
    __slots__ = ("attribute", "detail", "severity", "summary")
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[Diagnostic.Severity]
        ERROR: _ClassVar[Diagnostic.Severity]
        WARNING: _ClassVar[Diagnostic.Severity]

    INVALID: Diagnostic.Severity
    ERROR: Diagnostic.Severity
    WARNING: Diagnostic.Severity
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    severity: Diagnostic.Severity
    summary: str
    detail: str
    attribute: AttributePath
    def __init__(
        self,
        severity: Diagnostic.Severity | str | None = ...,
        summary: str | None = ...,
        detail: str | None = ...,
        attribute: AttributePath | _Mapping | None = ...,
    ) -> None: ...

class FunctionError(_message.Message):
    __slots__ = ("function_argument", "text")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_ARGUMENT_FIELD_NUMBER: _ClassVar[int]
    text: str
    function_argument: int
    def __init__(self, text: str | None = ..., function_argument: int | None = ...) -> None: ...

class AttributePath(_message.Message):
    __slots__ = ("steps",)
    class Step(_message.Message):
        __slots__ = ("attribute_name", "element_key_int", "element_key_string")
        ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
        ELEMENT_KEY_STRING_FIELD_NUMBER: _ClassVar[int]
        ELEMENT_KEY_INT_FIELD_NUMBER: _ClassVar[int]
        attribute_name: str
        element_key_string: str
        element_key_int: int
        def __init__(
            self,
            attribute_name: str | None = ...,
            element_key_string: str | None = ...,
            element_key_int: int | None = ...,
        ) -> None: ...

    STEPS_FIELD_NUMBER: _ClassVar[int]
    steps: _containers.RepeatedCompositeFieldContainer[AttributePath.Step]
    def __init__(self, steps: _Iterable[AttributePath.Step | _Mapping] | None = ...) -> None: ...

class StopProvider(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class Response(_message.Message):
        __slots__ = ("Error",)
        ERROR_FIELD_NUMBER: _ClassVar[int]
        Error: str
        def __init__(self, Error: str | None = ...) -> None: ...

    def __init__(self) -> None: ...

class RawState(_message.Message):
    __slots__ = ("flatmap", "json")
    class FlatmapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: str | None = ..., value: str | None = ...) -> None: ...

    JSON_FIELD_NUMBER: _ClassVar[int]
    FLATMAP_FIELD_NUMBER: _ClassVar[int]
    json: bytes
    flatmap: _containers.ScalarMap[str, str]
    def __init__(self, json: bytes | None = ..., flatmap: _Mapping[str, str] | None = ...) -> None: ...

class ResourceIdentitySchema(_message.Message):
    __slots__ = ("identity_attributes", "version")
    class IdentityAttribute(_message.Message):
        __slots__ = (
            "description",
            "name",
            "optional_for_import",
            "required_for_import",
            "type",
        )
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        REQUIRED_FOR_IMPORT_FIELD_NUMBER: _ClassVar[int]
        OPTIONAL_FOR_IMPORT_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: bytes
        required_for_import: bool
        optional_for_import: bool
        description: str
        def __init__(
            self,
            name: str | None = ...,
            type: bytes | None = ...,
            required_for_import: bool = ...,
            optional_for_import: bool = ...,
            description: str | None = ...,
        ) -> None: ...

    VERSION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    version: int
    identity_attributes: _containers.RepeatedCompositeFieldContainer[ResourceIdentitySchema.IdentityAttribute]
    def __init__(
        self,
        version: int | None = ...,
        identity_attributes: _Iterable[ResourceIdentitySchema.IdentityAttribute | _Mapping] | None = ...,
    ) -> None: ...

class ResourceIdentityData(_message.Message):
    __slots__ = ("identity_data",)
    IDENTITY_DATA_FIELD_NUMBER: _ClassVar[int]
    identity_data: DynamicValue
    def __init__(self, identity_data: DynamicValue | _Mapping | None = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ("block", "version")
    class Block(_message.Message):
        __slots__ = (
            "attributes",
            "block_types",
            "deprecated",
            "description",
            "description_kind",
            "version",
        )
        VERSION_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        BLOCK_TYPES_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_KIND_FIELD_NUMBER: _ClassVar[int]
        DEPRECATED_FIELD_NUMBER: _ClassVar[int]
        version: int
        attributes: _containers.RepeatedCompositeFieldContainer[Schema.Attribute]
        block_types: _containers.RepeatedCompositeFieldContainer[Schema.NestedBlock]
        description: str
        description_kind: StringKind
        deprecated: bool
        def __init__(
            self,
            version: int | None = ...,
            attributes: _Iterable[Schema.Attribute | _Mapping] | None = ...,
            block_types: _Iterable[Schema.NestedBlock | _Mapping] | None = ...,
            description: str | None = ...,
            description_kind: StringKind | str | None = ...,
            deprecated: bool = ...,
        ) -> None: ...

    class Attribute(_message.Message):
        __slots__ = (
            "computed",
            "deprecated",
            "description",
            "description_kind",
            "name",
            "nested_type",
            "optional",
            "required",
            "sensitive",
            "type",
            "write_only",
        )
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NESTED_TYPE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        REQUIRED_FIELD_NUMBER: _ClassVar[int]
        OPTIONAL_FIELD_NUMBER: _ClassVar[int]
        COMPUTED_FIELD_NUMBER: _ClassVar[int]
        SENSITIVE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_KIND_FIELD_NUMBER: _ClassVar[int]
        DEPRECATED_FIELD_NUMBER: _ClassVar[int]
        WRITE_ONLY_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: bytes
        nested_type: Schema.Object
        description: str
        required: bool
        optional: bool
        computed: bool
        sensitive: bool
        description_kind: StringKind
        deprecated: bool
        write_only: bool
        def __init__(
            self,
            name: str | None = ...,
            type: bytes | None = ...,
            nested_type: Schema.Object | _Mapping | None = ...,
            description: str | None = ...,
            required: bool = ...,
            optional: bool = ...,
            computed: bool = ...,
            sensitive: bool = ...,
            description_kind: StringKind | str | None = ...,
            deprecated: bool = ...,
            write_only: bool = ...,
        ) -> None: ...

    class NestedBlock(_message.Message):
        __slots__ = ("block", "max_items", "min_items", "nesting", "type_name")
        class NestingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            INVALID: _ClassVar[Schema.NestedBlock.NestingMode]
            SINGLE: _ClassVar[Schema.NestedBlock.NestingMode]
            LIST: _ClassVar[Schema.NestedBlock.NestingMode]
            SET: _ClassVar[Schema.NestedBlock.NestingMode]
            MAP: _ClassVar[Schema.NestedBlock.NestingMode]
            GROUP: _ClassVar[Schema.NestedBlock.NestingMode]

        INVALID: Schema.NestedBlock.NestingMode
        SINGLE: Schema.NestedBlock.NestingMode
        LIST: Schema.NestedBlock.NestingMode
        SET: Schema.NestedBlock.NestingMode
        MAP: Schema.NestedBlock.NestingMode
        GROUP: Schema.NestedBlock.NestingMode
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        BLOCK_FIELD_NUMBER: _ClassVar[int]
        NESTING_FIELD_NUMBER: _ClassVar[int]
        MIN_ITEMS_FIELD_NUMBER: _ClassVar[int]
        MAX_ITEMS_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        block: Schema.Block
        nesting: Schema.NestedBlock.NestingMode
        min_items: int
        max_items: int
        def __init__(
            self,
            type_name: str | None = ...,
            block: Schema.Block | _Mapping | None = ...,
            nesting: Schema.NestedBlock.NestingMode | str | None = ...,
            min_items: int | None = ...,
            max_items: int | None = ...,
        ) -> None: ...

    class Object(_message.Message):
        __slots__ = ("attributes", "max_items", "min_items", "nesting")
        class NestingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            INVALID: _ClassVar[Schema.Object.NestingMode]
            SINGLE: _ClassVar[Schema.Object.NestingMode]
            LIST: _ClassVar[Schema.Object.NestingMode]
            SET: _ClassVar[Schema.Object.NestingMode]
            MAP: _ClassVar[Schema.Object.NestingMode]

        INVALID: Schema.Object.NestingMode
        SINGLE: Schema.Object.NestingMode
        LIST: Schema.Object.NestingMode
        SET: Schema.Object.NestingMode
        MAP: Schema.Object.NestingMode
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        NESTING_FIELD_NUMBER: _ClassVar[int]
        MIN_ITEMS_FIELD_NUMBER: _ClassVar[int]
        MAX_ITEMS_FIELD_NUMBER: _ClassVar[int]
        attributes: _containers.RepeatedCompositeFieldContainer[Schema.Attribute]
        nesting: Schema.Object.NestingMode
        min_items: int
        max_items: int
        def __init__(
            self,
            attributes: _Iterable[Schema.Attribute | _Mapping] | None = ...,
            nesting: Schema.Object.NestingMode | str | None = ...,
            min_items: int | None = ...,
            max_items: int | None = ...,
        ) -> None: ...

    VERSION_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    version: int
    block: Schema.Block
    def __init__(self, version: int | None = ..., block: Schema.Block | _Mapping | None = ...) -> None: ...

class Function(_message.Message):
    __slots__ = (
        "deprecation_message",
        "description",
        "description_kind",
        "parameters",
        "summary",
        "variadic_parameter",
    )
    class Parameter(_message.Message):
        __slots__ = (
            "allow_null_value",
            "allow_unknown_values",
            "description",
            "description_kind",
            "name",
            "type",
        )
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        ALLOW_NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
        ALLOW_UNKNOWN_VALUES_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_KIND_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: bytes
        allow_null_value: bool
        allow_unknown_values: bool
        description: str
        description_kind: StringKind
        def __init__(
            self,
            name: str | None = ...,
            type: bytes | None = ...,
            allow_null_value: bool = ...,
            allow_unknown_values: bool = ...,
            description: str | None = ...,
            description_kind: StringKind | str | None = ...,
        ) -> None: ...

    class Return(_message.Message):
        __slots__ = ("type",)
        TYPE_FIELD_NUMBER: _ClassVar[int]
        type: bytes
        def __init__(self, type: bytes | None = ...) -> None: ...

    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VARIADIC_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    RETURN_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_KIND_FIELD_NUMBER: _ClassVar[int]
    DEPRECATION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[Function.Parameter]
    variadic_parameter: Function.Parameter
    summary: str
    description: str
    description_kind: StringKind
    deprecation_message: str
    def __init__(
        self,
        parameters: _Iterable[Function.Parameter | _Mapping] | None = ...,
        variadic_parameter: Function.Parameter | _Mapping | None = ...,
        summary: str | None = ...,
        description: str | None = ...,
        description_kind: StringKind | str | None = ...,
        deprecation_message: str | None = ...,
        **kwargs: Any,
    ) -> None: ...

class ServerCapabilities(_message.Message):
    __slots__ = ("get_provider_schema_optional", "move_resource_state", "plan_destroy")
    PLAN_DESTROY_FIELD_NUMBER: _ClassVar[int]
    GET_PROVIDER_SCHEMA_OPTIONAL_FIELD_NUMBER: _ClassVar[int]
    MOVE_RESOURCE_STATE_FIELD_NUMBER: _ClassVar[int]
    plan_destroy: bool
    get_provider_schema_optional: bool
    move_resource_state: bool
    def __init__(
        self,
        plan_destroy: bool = ...,
        get_provider_schema_optional: bool = ...,
        move_resource_state: bool = ...,
    ) -> None: ...

class ClientCapabilities(_message.Message):
    __slots__ = ("deferral_allowed", "write_only_attributes_allowed")
    DEFERRAL_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    WRITE_ONLY_ATTRIBUTES_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    deferral_allowed: bool
    write_only_attributes_allowed: bool
    def __init__(self, deferral_allowed: bool = ..., write_only_attributes_allowed: bool = ...) -> None: ...

class Deferred(_message.Message):
    __slots__ = ("reason",)
    class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Deferred.Reason]
        RESOURCE_CONFIG_UNKNOWN: _ClassVar[Deferred.Reason]
        PROVIDER_CONFIG_UNKNOWN: _ClassVar[Deferred.Reason]
        ABSENT_PREREQ: _ClassVar[Deferred.Reason]

    UNKNOWN: Deferred.Reason
    RESOURCE_CONFIG_UNKNOWN: Deferred.Reason
    PROVIDER_CONFIG_UNKNOWN: Deferred.Reason
    ABSENT_PREREQ: Deferred.Reason
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: Deferred.Reason
    def __init__(self, reason: Deferred.Reason | str | None = ...) -> None: ...

class GetMetadata(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class Response(_message.Message):
        __slots__ = (
            "data_sources",
            "diagnostics",
            "ephemeral_resources",
            "functions",
            "resources",
            "server_capabilities",
        )
        SERVER_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
        RESOURCES_FIELD_NUMBER: _ClassVar[int]
        FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
        EPHEMERAL_RESOURCES_FIELD_NUMBER: _ClassVar[int]
        server_capabilities: ServerCapabilities
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        data_sources: _containers.RepeatedCompositeFieldContainer[GetMetadata.DataSourceMetadata]
        resources: _containers.RepeatedCompositeFieldContainer[GetMetadata.ResourceMetadata]
        functions: _containers.RepeatedCompositeFieldContainer[GetMetadata.FunctionMetadata]
        ephemeral_resources: _containers.RepeatedCompositeFieldContainer[GetMetadata.EphemeralMetadata]
        def __init__(
            self,
            server_capabilities: ServerCapabilities | _Mapping | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            data_sources: _Iterable[GetMetadata.DataSourceMetadata | _Mapping] | None = ...,
            resources: _Iterable[GetMetadata.ResourceMetadata | _Mapping] | None = ...,
            functions: _Iterable[GetMetadata.FunctionMetadata | _Mapping] | None = ...,
            ephemeral_resources: _Iterable[GetMetadata.EphemeralMetadata | _Mapping] | None = ...,
        ) -> None: ...

    class EphemeralMetadata(_message.Message):
        __slots__ = ("type_name",)
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        def __init__(self, type_name: str | None = ...) -> None: ...

    class FunctionMetadata(_message.Message):
        __slots__ = ("name",)
        NAME_FIELD_NUMBER: _ClassVar[int]
        name: str
        def __init__(self, name: str | None = ...) -> None: ...

    class DataSourceMetadata(_message.Message):
        __slots__ = ("type_name",)
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        def __init__(self, type_name: str | None = ...) -> None: ...

    class ResourceMetadata(_message.Message):
        __slots__ = ("type_name",)
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        def __init__(self, type_name: str | None = ...) -> None: ...

    def __init__(self) -> None: ...

class GetProviderSchema(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class Response(_message.Message):
        __slots__ = (
            "data_source_schemas",
            "diagnostics",
            "ephemeral_resource_schemas",
            "functions",
            "provider",
            "provider_meta",
            "resource_schemas",
            "server_capabilities",
        )
        class ResourceSchemasEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Schema
            def __init__(self, key: str | None = ..., value: Schema | _Mapping | None = ...) -> None: ...

        class DataSourceSchemasEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Schema
            def __init__(self, key: str | None = ..., value: Schema | _Mapping | None = ...) -> None: ...

        class FunctionsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Function
            def __init__(self, key: str | None = ..., value: Function | _Mapping | None = ...) -> None: ...

        class EphemeralResourceSchemasEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Schema
            def __init__(self, key: str | None = ..., value: Schema | _Mapping | None = ...) -> None: ...

        PROVIDER_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_SCHEMAS_FIELD_NUMBER: _ClassVar[int]
        DATA_SOURCE_SCHEMAS_FIELD_NUMBER: _ClassVar[int]
        FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
        EPHEMERAL_RESOURCE_SCHEMAS_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        SERVER_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        provider: Schema
        resource_schemas: _containers.MessageMap[str, Schema]
        data_source_schemas: _containers.MessageMap[str, Schema]
        functions: _containers.MessageMap[str, Function]
        ephemeral_resource_schemas: _containers.MessageMap[str, Schema]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        provider_meta: Schema
        server_capabilities: ServerCapabilities
        def __init__(
            self,
            provider: Schema | _Mapping | None = ...,
            resource_schemas: _Mapping[str, Schema] | None = ...,
            data_source_schemas: _Mapping[str, Schema] | None = ...,
            functions: _Mapping[str, Function] | None = ...,
            ephemeral_resource_schemas: _Mapping[str, Schema] | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            provider_meta: Schema | _Mapping | None = ...,
            server_capabilities: ServerCapabilities | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class ValidateProviderConfig(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("config",)
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        config: DynamicValue
        def __init__(self, config: DynamicValue | _Mapping | None = ...) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics",)
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...) -> None: ...

    def __init__(self) -> None: ...

class UpgradeResourceState(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("raw_state", "type_name", "version")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        RAW_STATE_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        version: int
        raw_state: RawState
        def __init__(
            self,
            type_name: str | None = ...,
            version: int | None = ...,
            raw_state: RawState | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics", "upgraded_state")
        UPGRADED_STATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        upgraded_state: DynamicValue
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(
            self,
            upgraded_state: DynamicValue | _Mapping | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class GetResourceIdentitySchemas(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics", "identity_schemas")
        class IdentitySchemasEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: ResourceIdentitySchema
            def __init__(
                self,
                key: str | None = ...,
                value: ResourceIdentitySchema | _Mapping | None = ...,
            ) -> None: ...

        IDENTITY_SCHEMAS_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        identity_schemas: _containers.MessageMap[str, ResourceIdentitySchema]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(
            self,
            identity_schemas: _Mapping[str, ResourceIdentitySchema] | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class UpgradeResourceIdentity(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("raw_identity", "type_name", "version")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        RAW_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        version: int
        raw_identity: RawState
        def __init__(
            self,
            type_name: str | None = ...,
            version: int | None = ...,
            raw_identity: RawState | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics", "upgraded_identity")
        UPGRADED_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        upgraded_identity: ResourceIdentityData
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(
            self,
            upgraded_identity: ResourceIdentityData | _Mapping | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class ValidateResourceConfig(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("client_capabilities", "config", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        CLIENT_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        client_capabilities: ClientCapabilities
        def __init__(
            self,
            type_name: str | None = ...,
            config: DynamicValue | _Mapping | None = ...,
            client_capabilities: ClientCapabilities | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics",)
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...) -> None: ...

    def __init__(self) -> None: ...

class ValidateDataResourceConfig(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("config", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        def __init__(
            self,
            type_name: str | None = ...,
            config: DynamicValue | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics",)
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...) -> None: ...

    def __init__(self) -> None: ...

class ValidateEphemeralResourceConfig(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("config", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        def __init__(
            self,
            type_name: str | None = ...,
            config: DynamicValue | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics",)
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...) -> None: ...

    def __init__(self) -> None: ...

class ConfigureProvider(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("client_capabilities", "config", "terraform_version")
        TERRAFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        CLIENT_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        terraform_version: str
        config: DynamicValue
        client_capabilities: ClientCapabilities
        def __init__(
            self,
            terraform_version: str | None = ...,
            config: DynamicValue | _Mapping | None = ...,
            client_capabilities: ClientCapabilities | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics",)
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...) -> None: ...

    def __init__(self) -> None: ...

class ReadResource(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = (
            "client_capabilities",
            "current_identity",
            "current_state",
            "private",
            "provider_meta",
            "type_name",
        )
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        CLIENT_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        CURRENT_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        current_state: DynamicValue
        private: bytes
        provider_meta: DynamicValue
        client_capabilities: ClientCapabilities
        current_identity: ResourceIdentityData
        def __init__(
            self,
            type_name: str | None = ...,
            current_state: DynamicValue | _Mapping | None = ...,
            private: bytes | None = ...,
            provider_meta: DynamicValue | _Mapping | None = ...,
            client_capabilities: ClientCapabilities | _Mapping | None = ...,
            current_identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("deferred", "diagnostics", "new_identity", "new_state", "private")
        NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        DEFERRED_FIELD_NUMBER: _ClassVar[int]
        NEW_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        new_state: DynamicValue
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        private: bytes
        deferred: Deferred
        new_identity: ResourceIdentityData
        def __init__(
            self,
            new_state: DynamicValue | _Mapping | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            private: bytes | None = ...,
            deferred: Deferred | _Mapping | None = ...,
            new_identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class PlanResourceChange(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = (
            "client_capabilities",
            "config",
            "prior_identity",
            "prior_private",
            "prior_state",
            "proposed_new_state",
            "provider_meta",
            "type_name",
        )
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIOR_STATE_FIELD_NUMBER: _ClassVar[int]
        PROPOSED_NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        PRIOR_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        CLIENT_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        PRIOR_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        prior_state: DynamicValue
        proposed_new_state: DynamicValue
        config: DynamicValue
        prior_private: bytes
        provider_meta: DynamicValue
        client_capabilities: ClientCapabilities
        prior_identity: ResourceIdentityData
        def __init__(
            self,
            type_name: str | None = ...,
            prior_state: DynamicValue | _Mapping | None = ...,
            proposed_new_state: DynamicValue | _Mapping | None = ...,
            config: DynamicValue | _Mapping | None = ...,
            prior_private: bytes | None = ...,
            provider_meta: DynamicValue | _Mapping | None = ...,
            client_capabilities: ClientCapabilities | _Mapping | None = ...,
            prior_identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = (
            "deferred",
            "diagnostics",
            "legacy_type_system",
            "planned_identity",
            "planned_private",
            "planned_state",
            "requires_replace",
        )
        PLANNED_STATE_FIELD_NUMBER: _ClassVar[int]
        REQUIRES_REPLACE_FIELD_NUMBER: _ClassVar[int]
        PLANNED_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        LEGACY_TYPE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
        DEFERRED_FIELD_NUMBER: _ClassVar[int]
        PLANNED_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        planned_state: DynamicValue
        requires_replace: _containers.RepeatedCompositeFieldContainer[AttributePath]
        planned_private: bytes
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        legacy_type_system: bool
        deferred: Deferred
        planned_identity: ResourceIdentityData
        def __init__(
            self,
            planned_state: DynamicValue | _Mapping | None = ...,
            requires_replace: _Iterable[AttributePath | _Mapping] | None = ...,
            planned_private: bytes | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            legacy_type_system: bool = ...,
            deferred: Deferred | _Mapping | None = ...,
            planned_identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class ApplyResourceChange(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = (
            "config",
            "planned_identity",
            "planned_private",
            "planned_state",
            "prior_state",
            "provider_meta",
            "type_name",
        )
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIOR_STATE_FIELD_NUMBER: _ClassVar[int]
        PLANNED_STATE_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        PLANNED_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        PLANNED_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        prior_state: DynamicValue
        planned_state: DynamicValue
        config: DynamicValue
        planned_private: bytes
        provider_meta: DynamicValue
        planned_identity: ResourceIdentityData
        def __init__(
            self,
            type_name: str | None = ...,
            prior_state: DynamicValue | _Mapping | None = ...,
            planned_state: DynamicValue | _Mapping | None = ...,
            config: DynamicValue | _Mapping | None = ...,
            planned_private: bytes | None = ...,
            provider_meta: DynamicValue | _Mapping | None = ...,
            planned_identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = (
            "diagnostics",
            "legacy_type_system",
            "new_identity",
            "new_state",
            "private",
        )
        NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        LEGACY_TYPE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
        NEW_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        new_state: DynamicValue
        private: bytes
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        legacy_type_system: bool
        new_identity: ResourceIdentityData
        def __init__(
            self,
            new_state: DynamicValue | _Mapping | None = ...,
            private: bytes | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            legacy_type_system: bool = ...,
            new_identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class ImportResourceState(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("client_capabilities", "id", "identity", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        CLIENT_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        IDENTITY_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        id: str
        client_capabilities: ClientCapabilities
        identity: ResourceIdentityData
        def __init__(
            self,
            type_name: str | None = ...,
            id: str | None = ...,
            client_capabilities: ClientCapabilities | _Mapping | None = ...,
            identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    class ImportedResource(_message.Message):
        __slots__ = ("identity", "private", "state", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        IDENTITY_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        state: DynamicValue
        private: bytes
        identity: ResourceIdentityData
        def __init__(
            self,
            type_name: str | None = ...,
            state: DynamicValue | _Mapping | None = ...,
            private: bytes | None = ...,
            identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("deferred", "diagnostics", "imported_resources")
        IMPORTED_RESOURCES_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        DEFERRED_FIELD_NUMBER: _ClassVar[int]
        imported_resources: _containers.RepeatedCompositeFieldContainer[ImportResourceState.ImportedResource]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        deferred: Deferred
        def __init__(
            self,
            imported_resources: _Iterable[ImportResourceState.ImportedResource | _Mapping] | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            deferred: Deferred | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class MoveResourceState(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = (
            "source_identity",
            "source_identity_schema_version",
            "source_private",
            "source_provider_address",
            "source_schema_version",
            "source_state",
            "source_type_name",
            "target_type_name",
        )
        SOURCE_PROVIDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        SOURCE_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        SOURCE_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
        SOURCE_STATE_FIELD_NUMBER: _ClassVar[int]
        TARGET_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        SOURCE_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        SOURCE_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        SOURCE_IDENTITY_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
        source_provider_address: str
        source_type_name: str
        source_schema_version: int
        source_state: RawState
        target_type_name: str
        source_private: bytes
        source_identity: RawState
        source_identity_schema_version: int
        def __init__(
            self,
            source_provider_address: str | None = ...,
            source_type_name: str | None = ...,
            source_schema_version: int | None = ...,
            source_state: RawState | _Mapping | None = ...,
            target_type_name: str | None = ...,
            source_private: bytes | None = ...,
            source_identity: RawState | _Mapping | None = ...,
            source_identity_schema_version: int | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics", "target_identity", "target_private", "target_state")
        TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        TARGET_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        TARGET_IDENTITY_FIELD_NUMBER: _ClassVar[int]
        target_state: DynamicValue
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        target_private: bytes
        target_identity: ResourceIdentityData
        def __init__(
            self,
            target_state: DynamicValue | _Mapping | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            target_private: bytes | None = ...,
            target_identity: ResourceIdentityData | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class ReadDataSource(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("client_capabilities", "config", "provider_meta", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        CLIENT_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        provider_meta: DynamicValue
        client_capabilities: ClientCapabilities
        def __init__(
            self,
            type_name: str | None = ...,
            config: DynamicValue | _Mapping | None = ...,
            provider_meta: DynamicValue | _Mapping | None = ...,
            client_capabilities: ClientCapabilities | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("deferred", "diagnostics", "state")
        STATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        DEFERRED_FIELD_NUMBER: _ClassVar[int]
        state: DynamicValue
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        deferred: Deferred
        def __init__(
            self,
            state: DynamicValue | _Mapping | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            deferred: Deferred | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class OpenEphemeralResource(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("client_capabilities", "config", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        CLIENT_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        client_capabilities: ClientCapabilities
        def __init__(
            self,
            type_name: str | None = ...,
            config: DynamicValue | _Mapping | None = ...,
            client_capabilities: ClientCapabilities | _Mapping | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("deferred", "diagnostics", "private", "renew_at", "result")
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        RENEW_AT_FIELD_NUMBER: _ClassVar[int]
        RESULT_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        DEFERRED_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        renew_at: _timestamp_pb2.Timestamp
        result: DynamicValue
        private: bytes
        deferred: Deferred
        def __init__(
            self,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            renew_at: datetime.datetime | _timestamp_pb2.Timestamp | _Mapping | None = ...,
            result: DynamicValue | _Mapping | None = ...,
            private: bytes | None = ...,
            deferred: Deferred | _Mapping | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class RenewEphemeralResource(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("private", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        private: bytes
        def __init__(self, type_name: str | None = ..., private: bytes | None = ...) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics", "private", "renew_at")
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        RENEW_AT_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        renew_at: _timestamp_pb2.Timestamp
        private: bytes
        def __init__(
            self,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
            renew_at: datetime.datetime | _timestamp_pb2.Timestamp | _Mapping | None = ...,
            private: bytes | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class CloseEphemeralResource(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("private", "type_name")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        private: bytes
        def __init__(self, type_name: str | None = ..., private: bytes | None = ...) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics",)
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...) -> None: ...

    def __init__(self) -> None: ...

class GetFunctions(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class Response(_message.Message):
        __slots__ = ("diagnostics", "functions")
        class FunctionsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Function
            def __init__(self, key: str | None = ..., value: Function | _Mapping | None = ...) -> None: ...

        FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        functions: _containers.MessageMap[str, Function]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(
            self,
            functions: _Mapping[str, Function] | None = ...,
            diagnostics: _Iterable[Diagnostic | _Mapping] | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...

class CallFunction(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("arguments", "name")
        NAME_FIELD_NUMBER: _ClassVar[int]
        ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
        name: str
        arguments: _containers.RepeatedCompositeFieldContainer[DynamicValue]
        def __init__(
            self,
            name: str | None = ...,
            arguments: _Iterable[DynamicValue | _Mapping] | None = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ("error", "result")
        RESULT_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        result: DynamicValue
        error: FunctionError
        def __init__(
            self,
            result: DynamicValue | _Mapping | None = ...,
            error: FunctionError | _Mapping[Any, Any] | None = ...,
        ) -> None: ...

    def __init__(self) -> None: ...
