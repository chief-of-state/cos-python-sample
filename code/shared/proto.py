from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message
import logging

logger = logging.getLogger(__name__)

def pack_any(msg):
    any_message = Any()
    any_message.Pack(msg)
    return any_message

def unpack_any(any_message: Any, cls):
    assert isinstance(any_message, Any), f'any message required, got {type(any_message)}'
    assert isinstance(cls, type(Message)), "expecting proto class"

    output = cls()

    assert output.DESCRIPTOR.name in any_message.type_url, \
    f"cannot unpack {output.DESCRIPTOR.name} into {any_message.type_url}"

    any_message.Unpack(output)
    return output

def to_json(msg):
    return MessageToJson(msg)

def get_field(msg: Message, field_name):
    '''return field by name or None'''
    if msg.HasField(field_name):
        return msg.__getattribute__(field_name)
    return None
