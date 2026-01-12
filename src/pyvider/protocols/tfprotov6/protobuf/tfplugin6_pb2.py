# 
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'tfplugin6.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ftfplugin6.proto\x12\ttfplugin6\x1a\x1fgoogle/protobuf/timestamp.proto\"-\n\x0c\x44ynamicValue\x12\x0f\n\x07msgpack\x18\x01 \x01(\x0c\x12\x0c\n\x04json\x18\x02 \x01(\x0c\"\xbd\x01\n\nDiagnostic\x12\x30\n\x08severity\x18\x01 \x01(\x0e\x32\x1e.tfplugin6.Diagnostic.Severity\x12\x0f\n\x07summary\x18\x02 \x01(\t\x12\x0e\n\x06\x64\x65tail\x18\x03 \x01(\t\x12+\n\tattribute\x18\x04 \x01(\x0b\x32\x18.tfplugin6.AttributePath\"/\n\x08Severity\x12\x0b\n\x07INVALID\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x12\x0b\n\x07WARNING\x10\x02\"S\n\rFunctionError\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x1e\n\x11\x66unction_argument\x18\x02 \x01(\x03H\x00\x88\x01\x01\x42\x14\n\x12_function_argument\"\xa4\x01\n\rAttributePath\x12,\n\x05steps\x18\x01 \x03(\x0b\x32\x1d.tfplugin6.AttributePath.Step\x1a\x65\n\x04Step\x12\x18\n\x0e\x61ttribute_name\x18\x01 \x01(\tH\x00\x12\x1c\n\x12\x65lement_key_string\x18\x02 \x01(\tH\x00\x12\x19\n\x0f\x65lement_key_int\x18\x03 \x01(\x03H\x00\x42\n\n\x08selector\"4\n\x0cStopProvider\x1a\t\n\x07Request\x1a\x19\n\x08Response\x12\r\n\x05\x45rror\x18\x01 \x01(\t\"{\n\x08RawState\x12\x0c\n\x04json\x18\x01 \x01(\x0c\x12\x31\n\x07\x66latmap\x18\x02 \x03(\x0b\x32 .tfplugin6.RawState.FlatmapEntry\x1a.\n\x0c\x46latmapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xfb\x01\n\x16ResourceIdentitySchema\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12P\n\x13identity_attributes\x18\x02 \x03(\x0b\x32\x33.tfplugin6.ResourceIdentitySchema.IdentityAttribute\x1a~\n\x11IdentityAttribute\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\x0c\x12\x1b\n\x13required_for_import\x18\x03 \x01(\x08\x12\x1b\n\x13optional_for_import\x18\x04 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\"F\n\x14ResourceIdentityData\x12.\n\ridentity_data\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\"\x8c\x08\n\x06Schema\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12&\n\x05\x62lock\x18\x02 \x01(\x0b\x32\x17.tfplugin6.Schema.Block\x1a\xd7\x01\n\x05\x42lock\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12/\n\nattributes\x18\x02 \x03(\x0b\x32\x1b.tfplugin6.Schema.Attribute\x12\x32\n\x0b\x62lock_types\x18\x03 \x03(\x0b\x32\x1d.tfplugin6.Schema.NestedBlock\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12/\n\x10\x64\x65scription_kind\x18\x05 \x01(\x0e\x32\x15.tfplugin6.StringKind\x12\x12\n\ndeprecated\x18\x06 \x01(\x08\x1a\x8d\x02\n\tAttribute\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\x0c\x12-\n\x0bnested_type\x18\n \x01(\x0b\x32\x18.tfplugin6.Schema.Object\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x10\n\x08required\x18\x04 \x01(\x08\x12\x10\n\x08optional\x18\x05 \x01(\x08\x12\x10\n\x08\x63omputed\x18\x06 \x01(\x08\x12\x11\n\tsensitive\x18\x07 \x01(\x08\x12/\n\x10\x64\x65scription_kind\x18\x08 \x01(\x0e\x32\x15.tfplugin6.StringKind\x12\x12\n\ndeprecated\x18\t \x01(\x08\x12\x12\n\nwrite_only\x18\x0b \x01(\x08\x1a\xf9\x01\n\x0bNestedBlock\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12&\n\x05\x62lock\x18\x02 \x01(\x0b\x32\x17.tfplugin6.Schema.Block\x12:\n\x07nesting\x18\x03 \x01(\x0e\x32).tfplugin6.Schema.NestedBlock.NestingMode\x12\x11\n\tmin_items\x18\x04 \x01(\x03\x12\x11\n\tmax_items\x18\x05 \x01(\x03\"M\n\x0bNestingMode\x12\x0b\n\x07INVALID\x10\x00\x12\n\n\x06SINGLE\x10\x01\x12\x08\n\x04LIST\x10\x02\x12\x07\n\x03SET\x10\x03\x12\x07\n\x03MAP\x10\x04\x12\t\n\x05GROUP\x10\x05\x1a\xe2\x01\n\x06Object\x12/\n\nattributes\x18\x01 \x03(\x0b\x32\x1b.tfplugin6.Schema.Attribute\x12\x35\n\x07nesting\x18\x03 \x01(\x0e\x32$.tfplugin6.Schema.Object.NestingMode\x12\x15\n\tmin_items\x18\x04 \x01(\x03\x42\x02\x18\x01\x12\x15\n\tmax_items\x18\x05 \x01(\x03\x42\x02\x18\x01\"B\n\x0bNestingMode\x12\x0b\n\x07INVALID\x10\x00\x12\n\n\x06SINGLE\x10\x01\x12\x08\n\x04LIST\x10\x02\x12\x07\n\x03SET\x10\x03\x12\x07\n\x03MAP\x10\x04\"\xd8\x03\n\x08\x46unction\x12\x31\n\nparameters\x18\x01 \x03(\x0b\x32\x1d.tfplugin6.Function.Parameter\x12\x39\n\x12variadic_parameter\x18\x02 \x01(\x0b\x32\x1d.tfplugin6.Function.Parameter\x12*\n\x06return\x18\x03 \x01(\x0b\x32\x1a.tfplugin6.Function.Return\x12\x0f\n\x07summary\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12/\n\x10\x64\x65scription_kind\x18\x06 \x01(\x0e\x32\x15.tfplugin6.StringKind\x12\x1b\n\x13\x64\x65precation_message\x18\x07 \x01(\t\x1a\xa5\x01\n\tParameter\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\x0c\x12\x18\n\x10\x61llow_null_value\x18\x03 \x01(\x08\x12\x1c\n\x14\x61llow_unknown_values\x18\x04 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12/\n\x10\x64\x65scription_kind\x18\x06 \x01(\x0e\x32\x15.tfplugin6.StringKind\x1a\x16\n\x06Return\x12\x0c\n\x04type\x18\x01 \x01(\x0c\"m\n\x12ServerCapabilities\x12\x14\n\x0cplan_destroy\x18\x01 \x01(\x08\x12$\n\x1cget_provider_schema_optional\x18\x02 \x01(\x08\x12\x1b\n\x13move_resource_state\x18\x03 \x01(\x08\"U\n\x12\x43lientCapabilities\x12\x18\n\x10\x64\x65\x66\x65rral_allowed\x18\x01 \x01(\x08\x12%\n\x1dwrite_only_attributes_allowed\x18\x02 \x01(\x08\"\x9a\x01\n\x08\x44\x65\x66\x65rred\x12*\n\x06reason\x18\x01 \x01(\x0e\x32\x1a.tfplugin6.Deferred.Reason\"b\n\x06Reason\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x1b\n\x17RESOURCE_CONFIG_UNKNOWN\x10\x01\x12\x1b\n\x17PROVIDER_CONFIG_UNKNOWN\x10\x02\x12\x11\n\rABSENT_PREREQ\x10\x03\"\xa7\x04\n\x0bGetMetadata\x1a\t\n\x07Request\x1a\xf2\x02\n\x08Response\x12:\n\x13server_capabilities\x18\x01 \x01(\x0b\x32\x1d.tfplugin6.ServerCapabilities\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12?\n\x0c\x64\x61ta_sources\x18\x03 \x03(\x0b\x32).tfplugin6.GetMetadata.DataSourceMetadata\x12:\n\tresources\x18\x04 \x03(\x0b\x32\'.tfplugin6.GetMetadata.ResourceMetadata\x12:\n\tfunctions\x18\x05 \x03(\x0b\x32\'.tfplugin6.GetMetadata.FunctionMetadata\x12\x45\n\x13\x65phemeral_resources\x18\x06 \x03(\x0b\x32(.tfplugin6.GetMetadata.EphemeralMetadata\x1a&\n\x11\x45phemeralMetadata\x12\x11\n\ttype_name\x18\x01 \x01(\t\x1a \n\x10\x46unctionMetadata\x12\x0c\n\x04name\x18\x01 \x01(\t\x1a\'\n\x12\x44\x61taSourceMetadata\x12\x11\n\ttype_name\x18\x01 \x01(\t\x1a%\n\x10ResourceMetadata\x12\x11\n\ttype_name\x18\x01 \x01(\t\"\xf8\x06\n\x11GetProviderSchema\x1a\t\n\x07Request\x1a\xd7\x06\n\x08Response\x12#\n\x08provider\x18\x01 \x01(\x0b\x32\x11.tfplugin6.Schema\x12T\n\x10resource_schemas\x18\x02 \x03(\x0b\x32:.tfplugin6.GetProviderSchema.Response.ResourceSchemasEntry\x12Y\n\x13\x64\x61ta_source_schemas\x18\x03 \x03(\x0b\x32<.tfplugin6.GetProviderSchema.Response.DataSourceSchemasEntry\x12G\n\tfunctions\x18\x07 \x03(\x0b\x32\x34.tfplugin6.GetProviderSchema.Response.FunctionsEntry\x12g\n\x1a\x65phemeral_resource_schemas\x18\x08 \x03(\x0b\x32\x43.tfplugin6.GetProviderSchema.Response.EphemeralResourceSchemasEntry\x12*\n\x0b\x64iagnostics\x18\x04 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12(\n\rprovider_meta\x18\x05 \x01(\x0b\x32\x11.tfplugin6.Schema\x12:\n\x13server_capabilities\x18\x06 \x01(\x0b\x32\x1d.tfplugin6.ServerCapabilities\x1aI\n\x14ResourceSchemasEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.tfplugin6.Schema:\x02\x38\x01\x1aK\n\x16\x44\x61taSourceSchemasEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.tfplugin6.Schema:\x02\x38\x01\x1a\x45\n\x0e\x46unctionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.tfplugin6.Function:\x02\x38\x01\x1aR\n\x1d\x45phemeralResourceSchemasEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.tfplugin6.Schema:\x02\x38\x01\"\x84\x01\n\x16ValidateProviderConfig\x1a\x32\n\x07Request\x12\'\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x1a\x36\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\xd6\x01\n\x14UpgradeResourceState\x1aU\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x03\x12&\n\traw_state\x18\x03 \x01(\x0b\x32\x13.tfplugin6.RawState\x1ag\n\x08Response\x12/\n\x0eupgraded_state\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\x9a\x02\n\x1aGetResourceIdentitySchemas\x1a\t\n\x07Request\x1a\xf0\x01\n\x08Response\x12]\n\x10identity_schemas\x18\x01 \x03(\x0b\x32\x43.tfplugin6.GetResourceIdentitySchemas.Response.IdentitySchemasEntry\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x1aY\n\x14IdentitySchemasEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.tfplugin6.ResourceIdentitySchema:\x02\x38\x01\"\xe7\x01\n\x17UpgradeResourceIdentity\x1aX\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x03\x12)\n\x0craw_identity\x18\x03 \x01(\x0b\x32\x13.tfplugin6.RawState\x1ar\n\x08Response\x12:\n\x11upgraded_identity\x18\x01 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\xd4\x01\n\x16ValidateResourceConfig\x1a\x81\x01\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\'\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12:\n\x13\x63lient_capabilities\x18\x03 \x01(\x0b\x32\x1d.tfplugin6.ClientCapabilities\x1a\x36\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x01 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\x9b\x01\n\x1aValidateDataResourceConfig\x1a\x45\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\'\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x1a\x36\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x01 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\xa0\x01\n\x1fValidateEphemeralResourceConfig\x1a\x45\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\'\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x1a\x36\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x01 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\xd7\x01\n\x11\x43onfigureProvider\x1a\x89\x01\n\x07Request\x12\x19\n\x11terraform_version\x18\x01 \x01(\t\x12\'\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12:\n\x13\x63lient_capabilities\x18\x03 \x01(\x0b\x32\x1d.tfplugin6.ClientCapabilities\x1a\x36\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x01 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\xe9\x03\n\x0cReadResource\x1a\x84\x02\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12.\n\rcurrent_state\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x0f\n\x07private\x18\x03 \x01(\x0c\x12.\n\rprovider_meta\x18\x04 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12:\n\x13\x63lient_capabilities\x18\x05 \x01(\x0b\x32\x1d.tfplugin6.ClientCapabilities\x12\x39\n\x10\x63urrent_identity\x18\x06 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\x1a\xd1\x01\n\x08Response\x12*\n\tnew_state\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12\x0f\n\x07private\x18\x03 \x01(\x0c\x12%\n\x08\x64\x65\x66\x65rred\x18\x04 \x01(\x0b\x32\x13.tfplugin6.Deferred\x12\x35\n\x0cnew_identity\x18\x05 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\"\xaf\x05\n\x12PlanResourceChange\x1a\xe4\x02\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12,\n\x0bprior_state\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x33\n\x12proposed_new_state\x18\x03 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\'\n\x06\x63onfig\x18\x04 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x15\n\rprior_private\x18\x05 \x01(\x0c\x12.\n\rprovider_meta\x18\x06 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12:\n\x13\x63lient_capabilities\x18\x07 \x01(\x0b\x32\x1d.tfplugin6.ClientCapabilities\x12\x37\n\x0eprior_identity\x18\x08 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\x1a\xb1\x02\n\x08Response\x12.\n\rplanned_state\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x32\n\x10requires_replace\x18\x02 \x03(\x0b\x32\x18.tfplugin6.AttributePath\x12\x17\n\x0fplanned_private\x18\x03 \x01(\x0c\x12*\n\x0b\x64iagnostics\x18\x04 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12\x1a\n\x12legacy_type_system\x18\x05 \x01(\x08\x12%\n\x08\x64\x65\x66\x65rred\x18\x06 \x01(\x0b\x32\x13.tfplugin6.Deferred\x12\x39\n\x10planned_identity\x18\x07 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\"\x88\x04\n\x13\x41pplyResourceChange\x1a\xa7\x02\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12,\n\x0bprior_state\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12.\n\rplanned_state\x18\x03 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\'\n\x06\x63onfig\x18\x04 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x17\n\x0fplanned_private\x18\x05 \x01(\x0c\x12.\n\rprovider_meta\x18\x06 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x39\n\x10planned_identity\x18\x07 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\x1a\xc6\x01\n\x08Response\x12*\n\tnew_state\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x0f\n\x07private\x18\x02 \x01(\x0c\x12*\n\x0b\x64iagnostics\x18\x03 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12\x1a\n\x12legacy_type_system\x18\x04 \x01(\x08\x12\x35\n\x0cnew_identity\x18\x05 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\"\xf0\x03\n\x13ImportResourceState\x1a\x97\x01\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12:\n\x13\x63lient_capabilities\x18\x03 \x01(\x0b\x32\x1d.tfplugin6.ClientCapabilities\x12\x31\n\x08identity\x18\x04 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\x1a\x91\x01\n\x10ImportedResource\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12&\n\x05state\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x0f\n\x07private\x18\x03 \x01(\x0c\x12\x31\n\x08identity\x18\x04 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\x1a\xaa\x01\n\x08Response\x12K\n\x12imported_resources\x18\x01 \x03(\x0b\x32/.tfplugin6.ImportResourceState.ImportedResource\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12%\n\x08\x64\x65\x66\x65rred\x18\x03 \x01(\x0b\x32\x13.tfplugin6.Deferred\"\xe6\x03\n\x11MoveResourceState\x1a\x96\x02\n\x07Request\x12\x1f\n\x17source_provider_address\x18\x01 \x01(\t\x12\x18\n\x10source_type_name\x18\x02 \x01(\t\x12\x1d\n\x15source_schema_version\x18\x03 \x01(\x03\x12)\n\x0csource_state\x18\x04 \x01(\x0b\x32\x13.tfplugin6.RawState\x12\x18\n\x10target_type_name\x18\x05 \x01(\t\x12\x16\n\x0esource_private\x18\x06 \x01(\x0c\x12,\n\x0fsource_identity\x18\x07 \x01(\x0b\x32\x13.tfplugin6.RawState\x12&\n\x1esource_identity_schema_version\x18\x08 \x01(\x03\x1a\xb7\x01\n\x08Response\x12-\n\x0ctarget_state\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12\x16\n\x0etarget_private\x18\x03 \x01(\x0c\x12\x38\n\x0ftarget_identity\x18\x04 \x01(\x0b\x32\x1f.tfplugin6.ResourceIdentityData\"\xcc\x02\n\x0eReadDataSource\x1a\xb1\x01\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\'\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12.\n\rprovider_meta\x18\x03 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12:\n\x13\x63lient_capabilities\x18\x04 \x01(\x0b\x32\x1d.tfplugin6.ClientCapabilities\x1a\x85\x01\n\x08Response\x12&\n\x05state\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12%\n\x08\x64\x65\x66\x65rred\x18\x03 \x01(\x0b\x32\x13.tfplugin6.Deferred\"\x86\x03\n\x15OpenEphemeralResource\x1a\x81\x01\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\'\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12:\n\x13\x63lient_capabilities\x18\x03 \x01(\x0b\x32\x1d.tfplugin6.ClientCapabilities\x1a\xe8\x01\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x01 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12\x31\n\x08renew_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x12\'\n\x06result\x18\x03 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\x14\n\x07private\x18\x04 \x01(\x0cH\x01\x88\x01\x01\x12%\n\x08\x64\x65\x66\x65rred\x18\x05 \x01(\x0b\x32\x13.tfplugin6.DeferredB\x0b\n\t_renew_atB\n\n\x08_private\"\xf3\x01\n\x16RenewEphemeralResource\x1a>\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\x14\n\x07private\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x42\n\n\x08_private\x1a\x98\x01\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x01 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x12\x31\n\x08renew_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x12\x14\n\x07private\x18\x03 \x01(\x0cH\x01\x88\x01\x01\x42\x0b\n\t_renew_atB\n\n\x08_private\"\x90\x01\n\x16\x43loseEphemeralResource\x1a>\n\x07Request\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\x14\n\x07private\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x42\n\n\x08_private\x1a\x36\n\x08Response\x12*\n\x0b\x64iagnostics\x18\x01 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\"\xdd\x01\n\x0cGetFunctions\x1a\t\n\x07Request\x1a\xc1\x01\n\x08Response\x12\x42\n\tfunctions\x18\x01 \x03(\x0b\x32/.tfplugin6.GetFunctions.Response.FunctionsEntry\x12*\n\x0b\x64iagnostics\x18\x02 \x03(\x0b\x32\x15.tfplugin6.Diagnostic\x1a\x45\n\x0e\x46unctionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.tfplugin6.Function:\x02\x38\x01\"\xb1\x01\n\x0c\x43\x61llFunction\x1a\x43\n\x07Request\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\targuments\x18\x02 \x03(\x0b\x32\x17.tfplugin6.DynamicValue\x1a\\\n\x08Response\x12\'\n\x06result\x18\x01 \x01(\x0b\x32\x17.tfplugin6.DynamicValue\x12\'\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x18.tfplugin6.FunctionError*%\n\nStringKind\x12\t\n\x05PLAIN\x10\x00\x12\x0c\n\x08MARKDOWN\x10\x01\x32\xf2\x11\n\x08Provider\x12N\n\x0bGetMetadata\x12\x1e.tfplugin6.GetMetadata.Request\x1a\x1f.tfplugin6.GetMetadata.Response\x12`\n\x11GetProviderSchema\x12$.tfplugin6.GetProviderSchema.Request\x1a%.tfplugin6.GetProviderSchema.Response\x12o\n\x16ValidateProviderConfig\x12).tfplugin6.ValidateProviderConfig.Request\x1a*.tfplugin6.ValidateProviderConfig.Response\x12o\n\x16ValidateResourceConfig\x12).tfplugin6.ValidateResourceConfig.Request\x1a*.tfplugin6.ValidateResourceConfig.Response\x12{\n\x1aValidateDataResourceConfig\x12-.tfplugin6.ValidateDataResourceConfig.Request\x1a..tfplugin6.ValidateDataResourceConfig.Response\x12i\n\x14UpgradeResourceState\x12\'.tfplugin6.UpgradeResourceState.Request\x1a(.tfplugin6.UpgradeResourceState.Response\x12{\n\x1aGetResourceIdentitySchemas\x12-.tfplugin6.GetResourceIdentitySchemas.Request\x1a..tfplugin6.GetResourceIdentitySchemas.Response\x12r\n\x17UpgradeResourceIdentity\x12*.tfplugin6.UpgradeResourceIdentity.Request\x1a+.tfplugin6.UpgradeResourceIdentity.Response\x12`\n\x11\x43onfigureProvider\x12$.tfplugin6.ConfigureProvider.Request\x1a%.tfplugin6.ConfigureProvider.Response\x12Q\n\x0cReadResource\x12\x1f.tfplugin6.ReadResource.Request\x1a .tfplugin6.ReadResource.Response\x12\x63\n\x12PlanResourceChange\x12%.tfplugin6.PlanResourceChange.Request\x1a&.tfplugin6.PlanResourceChange.Response\x12\x66\n\x13\x41pplyResourceChange\x12&.tfplugin6.ApplyResourceChange.Request\x1a\'.tfplugin6.ApplyResourceChange.Response\x12\x66\n\x13ImportResourceState\x12&.tfplugin6.ImportResourceState.Request\x1a\'.tfplugin6.ImportResourceState.Response\x12`\n\x11MoveResourceState\x12$.tfplugin6.MoveResourceState.Request\x1a%.tfplugin6.MoveResourceState.Response\x12W\n\x0eReadDataSource\x12!.tfplugin6.ReadDataSource.Request\x1a\".tfplugin6.ReadDataSource.Response\x12\x8a\x01\n\x1fValidateEphemeralResourceConfig\x12\x32.tfplugin6.ValidateEphemeralResourceConfig.Request\x1a\x33.tfplugin6.ValidateEphemeralResourceConfig.Response\x12l\n\x15OpenEphemeralResource\x12(.tfplugin6.OpenEphemeralResource.Request\x1a).tfplugin6.OpenEphemeralResource.Response\x12o\n\x16RenewEphemeralResource\x12).tfplugin6.RenewEphemeralResource.Request\x1a*.tfplugin6.RenewEphemeralResource.Response\x12o\n\x16\x43loseEphemeralResource\x12).tfplugin6.CloseEphemeralResource.Request\x1a*.tfplugin6.CloseEphemeralResource.Response\x12Q\n\x0cGetFunctions\x12\x1f.tfplugin6.GetFunctions.Request\x1a .tfplugin6.GetFunctions.Response\x12Q\n\x0c\x43\x61llFunction\x12\x1f.tfplugin6.CallFunction.Request\x1a .tfplugin6.CallFunction.Response\x12Q\n\x0cStopProvider\x12\x1f.tfplugin6.StopProvider.Request\x1a .tfplugin6.StopProvider.ResponseB3Z1github.com/hashicorp/terraform/internal/tfplugin6b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tfplugin6_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z1github.com/hashicorp/terraform/internal/tfplugin6'
  _globals['_RAWSTATE_FLATMAPENTRY']._loaded_options = None
  _globals['_RAWSTATE_FLATMAPENTRY']._serialized_options = b'8\001'
  _globals['_SCHEMA_OBJECT'].fields_by_name['min_items']._loaded_options = None
  _globals['_SCHEMA_OBJECT'].fields_by_name['min_items']._serialized_options = b'\030\001'
  _globals['_SCHEMA_OBJECT'].fields_by_name['max_items']._loaded_options = None
  _globals['_SCHEMA_OBJECT'].fields_by_name['max_items']._serialized_options = b'\030\001'
  _globals['_GETPROVIDERSCHEMA_RESPONSE_RESOURCESCHEMASENTRY']._loaded_options = None
  _globals['_GETPROVIDERSCHEMA_RESPONSE_RESOURCESCHEMASENTRY']._serialized_options = b'8\001'
  _globals['_GETPROVIDERSCHEMA_RESPONSE_DATASOURCESCHEMASENTRY']._loaded_options = None
  _globals['_GETPROVIDERSCHEMA_RESPONSE_DATASOURCESCHEMASENTRY']._serialized_options = b'8\001'
  _globals['_GETPROVIDERSCHEMA_RESPONSE_FUNCTIONSENTRY']._loaded_options = None
  _globals['_GETPROVIDERSCHEMA_RESPONSE_FUNCTIONSENTRY']._serialized_options = b'8\001'
  _globals['_GETPROVIDERSCHEMA_RESPONSE_EPHEMERALRESOURCESCHEMASENTRY']._loaded_options = None
  _globals['_GETPROVIDERSCHEMA_RESPONSE_EPHEMERALRESOURCESCHEMASENTRY']._serialized_options = b'8\001'
  _globals['_GETRESOURCEIDENTITYSCHEMAS_RESPONSE_IDENTITYSCHEMASENTRY']._loaded_options = None
  _globals['_GETRESOURCEIDENTITYSCHEMAS_RESPONSE_IDENTITYSCHEMASENTRY']._serialized_options = b'8\001'
  _globals['_GETFUNCTIONS_RESPONSE_FUNCTIONSENTRY']._loaded_options = None
  _globals['_GETFUNCTIONS_RESPONSE_FUNCTIONSENTRY']._serialized_options = b'8\001'
  _globals['_STRINGKIND']._serialized_start=10216
  _globals['_STRINGKIND']._serialized_end=10253
  _globals['_DYNAMICVALUE']._serialized_start=63
  _globals['_DYNAMICVALUE']._serialized_end=108
  _globals['_DIAGNOSTIC']._serialized_start=111
  _globals['_DIAGNOSTIC']._serialized_end=300
  _globals['_DIAGNOSTIC_SEVERITY']._serialized_start=253
  _globals['_DIAGNOSTIC_SEVERITY']._serialized_end=300
  _globals['_FUNCTIONERROR']._serialized_start=302
  _globals['_FUNCTIONERROR']._serialized_end=385
  _globals['_ATTRIBUTEPATH']._serialized_start=388
  _globals['_ATTRIBUTEPATH']._serialized_end=552
  _globals['_ATTRIBUTEPATH_STEP']._serialized_start=451
  _globals['_ATTRIBUTEPATH_STEP']._serialized_end=552
  _globals['_STOPPROVIDER']._serialized_start=554
  _globals['_STOPPROVIDER']._serialized_end=606
  _globals['_STOPPROVIDER_REQUEST']._serialized_start=570
  _globals['_STOPPROVIDER_REQUEST']._serialized_end=579
  _globals['_STOPPROVIDER_RESPONSE']._serialized_start=581
  _globals['_STOPPROVIDER_RESPONSE']._serialized_end=606
  _globals['_RAWSTATE']._serialized_start=608
  _globals['_RAWSTATE']._serialized_end=731
  _globals['_RAWSTATE_FLATMAPENTRY']._serialized_start=685
  _globals['_RAWSTATE_FLATMAPENTRY']._serialized_end=731
  _globals['_RESOURCEIDENTITYSCHEMA']._serialized_start=734
  _globals['_RESOURCEIDENTITYSCHEMA']._serialized_end=985
  _globals['_RESOURCEIDENTITYSCHEMA_IDENTITYATTRIBUTE']._serialized_start=859
  _globals['_RESOURCEIDENTITYSCHEMA_IDENTITYATTRIBUTE']._serialized_end=985
  _globals['_RESOURCEIDENTITYDATA']._serialized_start=987
  _globals['_RESOURCEIDENTITYDATA']._serialized_end=1057
  _globals['_SCHEMA']._serialized_start=1060
  _globals['_SCHEMA']._serialized_end=2096
  _globals['_SCHEMA_BLOCK']._serialized_start=1128
  _globals['_SCHEMA_BLOCK']._serialized_end=1343
  _globals['_SCHEMA_ATTRIBUTE']._serialized_start=1346
  _globals['_SCHEMA_ATTRIBUTE']._serialized_end=1615
  _globals['_SCHEMA_NESTEDBLOCK']._serialized_start=1618
  _globals['_SCHEMA_NESTEDBLOCK']._serialized_end=1867
  _globals['_SCHEMA_NESTEDBLOCK_NESTINGMODE']._serialized_start=1790
  _globals['_SCHEMA_NESTEDBLOCK_NESTINGMODE']._serialized_end=1867
  _globals['_SCHEMA_OBJECT']._serialized_start=1870
  _globals['_SCHEMA_OBJECT']._serialized_end=2096
  _globals['_SCHEMA_OBJECT_NESTINGMODE']._serialized_start=1790
  _globals['_SCHEMA_OBJECT_NESTINGMODE']._serialized_end=1856
  _globals['_FUNCTION']._serialized_start=2099
  _globals['_FUNCTION']._serialized_end=2571
  _globals['_FUNCTION_PARAMETER']._serialized_start=2382
  _globals['_FUNCTION_PARAMETER']._serialized_end=2547
  _globals['_FUNCTION_RETURN']._serialized_start=2549
  _globals['_FUNCTION_RETURN']._serialized_end=2571
  _globals['_SERVERCAPABILITIES']._serialized_start=2573
  _globals['_SERVERCAPABILITIES']._serialized_end=2682
  _globals['_CLIENTCAPABILITIES']._serialized_start=2684
  _globals['_CLIENTCAPABILITIES']._serialized_end=2769
  _globals['_DEFERRED']._serialized_start=2772
  _globals['_DEFERRED']._serialized_end=2926
  _globals['_DEFERRED_REASON']._serialized_start=2828
  _globals['_DEFERRED_REASON']._serialized_end=2926
  _globals['_GETMETADATA']._serialized_start=2929
  _globals['_GETMETADATA']._serialized_end=3480
  _globals['_GETMETADATA_REQUEST']._serialized_start=570
  _globals['_GETMETADATA_REQUEST']._serialized_end=579
  _globals['_GETMETADATA_RESPONSE']._serialized_start=2956
  _globals['_GETMETADATA_RESPONSE']._serialized_end=3326
  _globals['_GETMETADATA_EPHEMERALMETADATA']._serialized_start=3328
  _globals['_GETMETADATA_EPHEMERALMETADATA']._serialized_end=3366
  _globals['_GETMETADATA_FUNCTIONMETADATA']._serialized_start=3368
  _globals['_GETMETADATA_FUNCTIONMETADATA']._serialized_end=3400
  _globals['_GETMETADATA_DATASOURCEMETADATA']._serialized_start=3402
  _globals['_GETMETADATA_DATASOURCEMETADATA']._serialized_end=3441
  _globals['_GETMETADATA_RESOURCEMETADATA']._serialized_start=3443
  _globals['_GETMETADATA_RESOURCEMETADATA']._serialized_end=3480
  _globals['_GETPROVIDERSCHEMA']._serialized_start=3483
  _globals['_GETPROVIDERSCHEMA']._serialized_end=4371
  _globals['_GETPROVIDERSCHEMA_REQUEST']._serialized_start=570
  _globals['_GETPROVIDERSCHEMA_REQUEST']._serialized_end=579
  _globals['_GETPROVIDERSCHEMA_RESPONSE']._serialized_start=3516
  _globals['_GETPROVIDERSCHEMA_RESPONSE']._serialized_end=4371
  _globals['_GETPROVIDERSCHEMA_RESPONSE_RESOURCESCHEMASENTRY']._serialized_start=4066
  _globals['_GETPROVIDERSCHEMA_RESPONSE_RESOURCESCHEMASENTRY']._serialized_end=4139
  _globals['_GETPROVIDERSCHEMA_RESPONSE_DATASOURCESCHEMASENTRY']._serialized_start=4141
  _globals['_GETPROVIDERSCHEMA_RESPONSE_DATASOURCESCHEMASENTRY']._serialized_end=4216
  _globals['_GETPROVIDERSCHEMA_RESPONSE_FUNCTIONSENTRY']._serialized_start=4218
  _globals['_GETPROVIDERSCHEMA_RESPONSE_FUNCTIONSENTRY']._serialized_end=4287
  _globals['_GETPROVIDERSCHEMA_RESPONSE_EPHEMERALRESOURCESCHEMASENTRY']._serialized_start=4289
  _globals['_GETPROVIDERSCHEMA_RESPONSE_EPHEMERALRESOURCESCHEMASENTRY']._serialized_end=4371
  _globals['_VALIDATEPROVIDERCONFIG']._serialized_start=4374
  _globals['_VALIDATEPROVIDERCONFIG']._serialized_end=4506
  _globals['_VALIDATEPROVIDERCONFIG_REQUEST']._serialized_start=4400
  _globals['_VALIDATEPROVIDERCONFIG_REQUEST']._serialized_end=4450
  _globals['_VALIDATEPROVIDERCONFIG_RESPONSE']._serialized_start=4452
  _globals['_VALIDATEPROVIDERCONFIG_RESPONSE']._serialized_end=4506
  _globals['_UPGRADERESOURCESTATE']._serialized_start=4509
  _globals['_UPGRADERESOURCESTATE']._serialized_end=4723
  _globals['_UPGRADERESOURCESTATE_REQUEST']._serialized_start=4533
  _globals['_UPGRADERESOURCESTATE_REQUEST']._serialized_end=4618
  _globals['_UPGRADERESOURCESTATE_RESPONSE']._serialized_start=4620
  _globals['_UPGRADERESOURCESTATE_RESPONSE']._serialized_end=4723
  _globals['_GETRESOURCEIDENTITYSCHEMAS']._serialized_start=4726
  _globals['_GETRESOURCEIDENTITYSCHEMAS']._serialized_end=5008
  _globals['_GETRESOURCEIDENTITYSCHEMAS_REQUEST']._serialized_start=570
  _globals['_GETRESOURCEIDENTITYSCHEMAS_REQUEST']._serialized_end=579
  _globals['_GETRESOURCEIDENTITYSCHEMAS_RESPONSE']._serialized_start=4768
  _globals['_GETRESOURCEIDENTITYSCHEMAS_RESPONSE']._serialized_end=5008
  _globals['_GETRESOURCEIDENTITYSCHEMAS_RESPONSE_IDENTITYSCHEMASENTRY']._serialized_start=4919
  _globals['_GETRESOURCEIDENTITYSCHEMAS_RESPONSE_IDENTITYSCHEMASENTRY']._serialized_end=5008
  _globals['_UPGRADERESOURCEIDENTITY']._serialized_start=5011
  _globals['_UPGRADERESOURCEIDENTITY']._serialized_end=5242
  _globals['_UPGRADERESOURCEIDENTITY_REQUEST']._serialized_start=5038
  _globals['_UPGRADERESOURCEIDENTITY_REQUEST']._serialized_end=5126
  _globals['_UPGRADERESOURCEIDENTITY_RESPONSE']._serialized_start=5128
  _globals['_UPGRADERESOURCEIDENTITY_RESPONSE']._serialized_end=5242
  _globals['_VALIDATERESOURCECONFIG']._serialized_start=5245
  _globals['_VALIDATERESOURCECONFIG']._serialized_end=5457
  _globals['_VALIDATERESOURCECONFIG_REQUEST']._serialized_start=5272
  _globals['_VALIDATERESOURCECONFIG_REQUEST']._serialized_end=5401
  _globals['_VALIDATERESOURCECONFIG_RESPONSE']._serialized_start=5403
  _globals['_VALIDATERESOURCECONFIG_RESPONSE']._serialized_end=5457
  _globals['_VALIDATEDATARESOURCECONFIG']._serialized_start=5460
  _globals['_VALIDATEDATARESOURCECONFIG']._serialized_end=5615
  _globals['_VALIDATEDATARESOURCECONFIG_REQUEST']._serialized_start=5272
  _globals['_VALIDATEDATARESOURCECONFIG_REQUEST']._serialized_end=5341
  _globals['_VALIDATEDATARESOURCECONFIG_RESPONSE']._serialized_start=5403
  _globals['_VALIDATEDATARESOURCECONFIG_RESPONSE']._serialized_end=5457
  _globals['_VALIDATEEPHEMERALRESOURCECONFIG']._serialized_start=5618
  _globals['_VALIDATEEPHEMERALRESOURCECONFIG']._serialized_end=5778
  _globals['_VALIDATEEPHEMERALRESOURCECONFIG_REQUEST']._serialized_start=5272
  _globals['_VALIDATEEPHEMERALRESOURCECONFIG_REQUEST']._serialized_end=5341
  _globals['_VALIDATEEPHEMERALRESOURCECONFIG_RESPONSE']._serialized_start=5403
  _globals['_VALIDATEEPHEMERALRESOURCECONFIG_RESPONSE']._serialized_end=5457
  _globals['_CONFIGUREPROVIDER']._serialized_start=5781
  _globals['_CONFIGUREPROVIDER']._serialized_end=5996
  _globals['_CONFIGUREPROVIDER_REQUEST']._serialized_start=5803
  _globals['_CONFIGUREPROVIDER_REQUEST']._serialized_end=5940
  _globals['_CONFIGUREPROVIDER_RESPONSE']._serialized_start=5403
  _globals['_CONFIGUREPROVIDER_RESPONSE']._serialized_end=5457
  _globals['_READRESOURCE']._serialized_start=5999
  _globals['_READRESOURCE']._serialized_end=6488
  _globals['_READRESOURCE_REQUEST']._serialized_start=6016
  _globals['_READRESOURCE_REQUEST']._serialized_end=6276
  _globals['_READRESOURCE_RESPONSE']._serialized_start=6279
  _globals['_READRESOURCE_RESPONSE']._serialized_end=6488
  _globals['_PLANRESOURCECHANGE']._serialized_start=6491
  _globals['_PLANRESOURCECHANGE']._serialized_end=7178
  _globals['_PLANRESOURCECHANGE_REQUEST']._serialized_start=6514
  _globals['_PLANRESOURCECHANGE_REQUEST']._serialized_end=6870
  _globals['_PLANRESOURCECHANGE_RESPONSE']._serialized_start=6873
  _globals['_PLANRESOURCECHANGE_RESPONSE']._serialized_end=7178
  _globals['_APPLYRESOURCECHANGE']._serialized_start=7181
  _globals['_APPLYRESOURCECHANGE']._serialized_end=7701
  _globals['_APPLYRESOURCECHANGE_REQUEST']._serialized_start=7205
  _globals['_APPLYRESOURCECHANGE_REQUEST']._serialized_end=7500
  _globals['_APPLYRESOURCECHANGE_RESPONSE']._serialized_start=7503
  _globals['_APPLYRESOURCECHANGE_RESPONSE']._serialized_end=7701
  _globals['_IMPORTRESOURCESTATE']._serialized_start=7704
  _globals['_IMPORTRESOURCESTATE']._serialized_end=8200
  _globals['_IMPORTRESOURCESTATE_REQUEST']._serialized_start=7728
  _globals['_IMPORTRESOURCESTATE_REQUEST']._serialized_end=7879
  _globals['_IMPORTRESOURCESTATE_IMPORTEDRESOURCE']._serialized_start=7882
  _globals['_IMPORTRESOURCESTATE_IMPORTEDRESOURCE']._serialized_end=8027
  _globals['_IMPORTRESOURCESTATE_RESPONSE']._serialized_start=8030
  _globals['_IMPORTRESOURCESTATE_RESPONSE']._serialized_end=8200
  _globals['_MOVERESOURCESTATE']._serialized_start=8203
  _globals['_MOVERESOURCESTATE']._serialized_end=8689
  _globals['_MOVERESOURCESTATE_REQUEST']._serialized_start=8225
  _globals['_MOVERESOURCESTATE_REQUEST']._serialized_end=8503
  _globals['_MOVERESOURCESTATE_RESPONSE']._serialized_start=8506
  _globals['_MOVERESOURCESTATE_RESPONSE']._serialized_end=8689
  _globals['_READDATASOURCE']._serialized_start=8692
  _globals['_READDATASOURCE']._serialized_end=9024
  _globals['_READDATASOURCE_REQUEST']._serialized_start=8711
  _globals['_READDATASOURCE_REQUEST']._serialized_end=8888
  _globals['_READDATASOURCE_RESPONSE']._serialized_start=8891
  _globals['_READDATASOURCE_RESPONSE']._serialized_end=9024
  _globals['_OPENEPHEMERALRESOURCE']._serialized_start=9027
  _globals['_OPENEPHEMERALRESOURCE']._serialized_end=9417
  _globals['_OPENEPHEMERALRESOURCE_REQUEST']._serialized_start=5272
  _globals['_OPENEPHEMERALRESOURCE_REQUEST']._serialized_end=5401
  _globals['_OPENEPHEMERALRESOURCE_RESPONSE']._serialized_start=9185
  _globals['_OPENEPHEMERALRESOURCE_RESPONSE']._serialized_end=9417
  _globals['_RENEWEPHEMERALRESOURCE']._serialized_start=9420
  _globals['_RENEWEPHEMERALRESOURCE']._serialized_end=9663
  _globals['_RENEWEPHEMERALRESOURCE_REQUEST']._serialized_start=9446
  _globals['_RENEWEPHEMERALRESOURCE_REQUEST']._serialized_end=9508
  _globals['_RENEWEPHEMERALRESOURCE_RESPONSE']._serialized_start=9511
  _globals['_RENEWEPHEMERALRESOURCE_RESPONSE']._serialized_end=9663
  _globals['_CLOSEEPHEMERALRESOURCE']._serialized_start=9666
  _globals['_CLOSEEPHEMERALRESOURCE']._serialized_end=9810
  _globals['_CLOSEEPHEMERALRESOURCE_REQUEST']._serialized_start=9446
  _globals['_CLOSEEPHEMERALRESOURCE_REQUEST']._serialized_end=9508
  _globals['_CLOSEEPHEMERALRESOURCE_RESPONSE']._serialized_start=5403
  _globals['_CLOSEEPHEMERALRESOURCE_RESPONSE']._serialized_end=5457
  _globals['_GETFUNCTIONS']._serialized_start=9813
  _globals['_GETFUNCTIONS']._serialized_end=10034
  _globals['_GETFUNCTIONS_REQUEST']._serialized_start=570
  _globals['_GETFUNCTIONS_REQUEST']._serialized_end=579
  _globals['_GETFUNCTIONS_RESPONSE']._serialized_start=9841
  _globals['_GETFUNCTIONS_RESPONSE']._serialized_end=10034
  _globals['_GETFUNCTIONS_RESPONSE_FUNCTIONSENTRY']._serialized_start=4218
  _globals['_GETFUNCTIONS_RESPONSE_FUNCTIONSENTRY']._serialized_end=4287
  _globals['_CALLFUNCTION']._serialized_start=10037
  _globals['_CALLFUNCTION']._serialized_end=10214
  _globals['_CALLFUNCTION_REQUEST']._serialized_start=10053
  _globals['_CALLFUNCTION_REQUEST']._serialized_end=10120
  _globals['_CALLFUNCTION_RESPONSE']._serialized_start=10122
  _globals['_CALLFUNCTION_RESPONSE']._serialized_end=10214
  _globals['_PROVIDER']._serialized_start=10256
  _globals['_PROVIDER']._serialized_end=12546
# @@protoc_insertion_point(module_scope)

# 🐍🏗️🔚
