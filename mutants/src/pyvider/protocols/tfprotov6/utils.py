import datetime

from google.protobuf.timestamp_pb2 import Timestamp
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


def x_datetime_to_proto__mutmut_orig(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is None:
        raise ValueError("datetime object must be timezone-aware.")
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def x_datetime_to_proto__mutmut_1(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is not None:
        raise ValueError("datetime object must be timezone-aware.")
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def x_datetime_to_proto__mutmut_2(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is None:
        raise ValueError(None)
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def x_datetime_to_proto__mutmut_3(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is None:
        raise ValueError("XXdatetime object must be timezone-aware.XX")
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def x_datetime_to_proto__mutmut_4(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is None:
        raise ValueError("DATETIME OBJECT MUST BE TIMEZONE-AWARE.")
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def x_datetime_to_proto__mutmut_5(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is None:
        raise ValueError("datetime object must be timezone-aware.")
    ts = None
    ts.FromDatetime(dt)
    return ts


def x_datetime_to_proto__mutmut_6(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is None:
        raise ValueError("datetime object must be timezone-aware.")
    ts = Timestamp()
    ts.FromDatetime(None)
    return ts

x_datetime_to_proto__mutmut_mutants : ClassVar[MutantDict] = {
'x_datetime_to_proto__mutmut_1': x_datetime_to_proto__mutmut_1, 
    'x_datetime_to_proto__mutmut_2': x_datetime_to_proto__mutmut_2, 
    'x_datetime_to_proto__mutmut_3': x_datetime_to_proto__mutmut_3, 
    'x_datetime_to_proto__mutmut_4': x_datetime_to_proto__mutmut_4, 
    'x_datetime_to_proto__mutmut_5': x_datetime_to_proto__mutmut_5, 
    'x_datetime_to_proto__mutmut_6': x_datetime_to_proto__mutmut_6
}

def datetime_to_proto(*args, **kwargs):
    result = _mutmut_trampoline(x_datetime_to_proto__mutmut_orig, x_datetime_to_proto__mutmut_mutants, args, kwargs)
    return result 

datetime_to_proto.__signature__ = _mutmut_signature(x_datetime_to_proto__mutmut_orig)
x_datetime_to_proto__mutmut_orig.__name__ = 'x_datetime_to_proto'
