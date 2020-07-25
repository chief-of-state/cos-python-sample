import logging
from google.protobuf.json_format import MessageToJson
from chief_of_state.readside_pb2_grpc import ReadSideHandlerServiceServicer
from chief_of_state.readside_pb2 import HandleReadSideRequest, HandleReadSideResponse
from sample_app.events_pb2 import *
from sample_app.state_pb2 import *
from cos_helpers.proto import ProtoHelper

logger = logging.getLogger(__name__)

class ReadSideHandlerImpl(ReadSideHandlerServiceServicer):

    def HandleReadSide(self, request, context):
        logger.info("received event")
        # logger.info(request)
        logger.info(ProtoHelper.to_json(request))
        return HandleReadSideResponse(successful=True)
