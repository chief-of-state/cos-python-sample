import logging
from chief_of_state.v1.readside_pb2_grpc import ReadSideHandlerServiceServicer
from chief_of_state.v1.readside_pb2 import HandleReadSideRequest, HandleReadSideResponse
from shared.proto import to_json
from banking_app.events_pb2 import *
from banking_app.state_pb2 import *


logger = logging.getLogger(__name__)

class ReadSideHandlerImpl(ReadSideHandlerServiceServicer):
    '''read side that logs event JSON to stdout'''

    def HandleReadSide(self, request, context):
        logger.info("received event")
        logger.info(to_json(request))
        return HandleReadSideResponse(successful=True)
