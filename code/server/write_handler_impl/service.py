import logging
from google.protobuf.json_format import MessageToJson
from grpc import StatusCode
from chief_of_state.writeside_pb2_grpc import WriteSideHandlerServiceServicer
from chief_of_state.writeside_pb2 import HandleCommandRequest, HandleEventRequest
from .command_handler import CommandHandler
from .event_handler import EventHandler


logger = logging.getLogger(__name__)

class WriteSideHandlerImpl(WriteSideHandlerServiceServicer):

    def HandleCommand(self, request, context):
        logger.info("WriteSideHandlerImpl.HandleCommand")
        assert isinstance(request, HandleCommandRequest)

        # create event from request
        try:
            response = CommandHandler.handle_command(
                command = request.command,
                current_state = request.current_state,
                meta = request.meta
            )

            return response

        except Exception as e:
            if isinstance(e, AssertionError):
                logger.error(f'invalid command, {e}')
                context.abort(StatusCode.INVALID_ARGUMENT, f'invalid command, {e}')
            else:
                raise e


    def HandleEvent(self, request, context):
        logger.info("WriteSideHandlerImpl.HandleEvent")
        assert isinstance(request, HandleEventRequest)

        # given event and prior state, build a new state
        # this should never fail!
        response = EventHandler.handle_event(
            event = request.event,
            current_state = request.current_state,
            meta = request.meta
        )

        return response
