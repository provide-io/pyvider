import datetime

from google.protobuf.timestamp_pb2 import Timestamp


def datetime_to_proto(dt: datetime.datetime) -> Timestamp:
    """Converts a Python UTC datetime object to a Protobuf Timestamp."""
    if dt.tzinfo is None:
        raise ValueError("datetime object must be timezone-aware.")
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts
