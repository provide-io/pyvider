# pyvider/common/utils/__init__.py
from pyvider.common.utils.attrs_factory import create_attrs_class_from_schema
from pyvider.common.utils.availability import HAS_MSGPACK

__all__ = ["HAS_MSGPACK", "create_attrs_class_from_schema"]
