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
        try:
            return CosClient.process_command(request.id, request)
        except Exception as e:
            print(e.code())
            print("DETAILS ******")
            print(e.details())
            logger.error(f'cos failed, code=({e.code()}), details=({e.details()})')
            raise e

    def GetCall(self, request, context):
        logger.info("SampleServiceImpl.GetCall")
        # send to chief of state, get resulting state
        return CosClient.get_state(request.id)
