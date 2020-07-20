import logging
from google.protobuf.json_format import MessageToJson
from sample_app.api_pb2_grpc import SampleServiceServicer
from .validation import StatelessValidation
from .cos_client import CosClient


logger = logging.getLogger(__name__)

class SampleServiceImpl(SampleServiceServicer):

    def CreateCall(self, request, context):
        logger.info("SampleServiceImpl.CreateCall")
        # do stateless validation
        StatelessValidation.validate(request)
        # send to chief of state, get resulting state
        return CosClient.process_command(request.id, request)

    def AppendCall(self, request, context):
        logger.info("SampleServiceImpl.AppendCall")
        # do stateless validation
        StatelessValidation.validate(request)
        # send to chief of state, get resulting state
        return CosClient.process_command(request.id, request)

    def GetCall(self, request, context):
        logger.info("SampleServiceImpl.GetCall")
        # send to chief of state, get resulting state
        return CosClient.process_command(request.id, request)
