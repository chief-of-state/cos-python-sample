import logging
from chief_of_state.v1.readside_pb2_grpc import ReadSideHandlerServiceServicer
from chief_of_state.v1.readside_pb2 import HandleReadSideRequest, HandleReadSideResponse
from cos_helpers.proto import ProtoHelper
from sample_app.events_pb2 import *
from sample_app.state_pb2 import *


logger = logging.getLogger(__name__)

class ReadSideHandlerImpl(ReadSideHandlerServiceServicer):
    '''read side that logs event JSON to stdout'''

    def HandleReadSide(self, request, context):
        logger.info("received event")
        logger.info(ProtoHelper.to_json(request))
        return HandleReadSideResponse(successful=True)
