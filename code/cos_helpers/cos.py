from chief_of_state.v1.writeside_pb2 import PersistAndReply, Reply, HandleEventResponse
from chief_of_state.v1.writeside_pb2 import HandleCommandResponse, HandleEventResponse
from google.protobuf.any_pb2 import Any


class CosEventReplyTypes():
    @staticmethod
    def persist_and_reply(event):
        '''wrap event in command response with COS instruction PersistAndReply'''
        any_event = Any()
        any_event.Pack(event)

        persist_and_reply = PersistAndReply()
        persist_and_reply.event.CopyFrom(any_event)

        response = HandleCommandResponse(persist_and_reply=persist_and_reply)

        return response

    @staticmethod
    def reply():
        '''helper method for generating a reply message'''
        return HandleCommandResponse(reply=Reply())
