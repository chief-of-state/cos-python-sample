from chief_of_state.v1.writeside_pb2 import HandleCommandResponse
from google.protobuf.any_pb2 import Any


class CosCommandResponses():
    @staticmethod
    def event(event):
        '''helper method for generating an event message'''
        any_event = Any()
        any_event.Pack(event)
        response = HandleCommandResponse(event=any_event)
        return response

    @staticmethod
    def no_event():
        '''helper method for generating a no event message'''
        return HandleCommandResponse()
