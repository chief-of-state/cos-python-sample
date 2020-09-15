import logging
from google.protobuf.json_format import MessageToJson
from grpc import StatusCode
from chief_of_state.v1.writeside_pb2_grpc import WriteSideHandlerServiceServicer
from chief_of_state.v1.writeside_pb2 import HandleCommandRequest, HandleEventRequest
from .command_handler import CommandHandler
from .event_handler import EventHandler

logger = logging.getLogger(__name__)

class WriteSideHandlerImpl(WriteSideHandlerServiceServicer):

    def HandleCommand(self, request: HandleCommandRequest, context):
        logger.info("WriteSideHandlerImpl.HandleCommand")
        # create event from request
        return CommandHandler(context).handle_command(request)

    def HandleEvent(self, request: HandleEventRequest, context):
        logger.info("WriteSideHandlerImpl.HandleEvent")
        # given event and prior state, build a new state
        # this should never fail!
        return EventHandler.handle_event(request)
