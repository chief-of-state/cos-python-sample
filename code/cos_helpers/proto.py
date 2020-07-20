from google.protobuf.any_pb2 import Any
from google.protobuf.json_format import MessageToJson

class ProtoHelper():
    @staticmethod
    def pack_any(msg):
        any_message = Any()
        any_message.Pack(msg)
        return any_message

    @staticmethod
    def unpack_any(any_message, cls):
        assert isinstance(any_message, Any), f'any message required, got {type(any_message)}'
        output = cls()
        any_message.Unpack(output)
        return output

    @staticmethod
    def to_json(msg):
        return MessageToJson(msg)
