import logging
from google.protobuf.json_format import MessageToJson
from sample_app.api_pb2_grpc import SampleServiceServicer
from .validation import StatelessValidation
from .cos_client import CosClient
from grpc import StatusCode
from sample_app.state_pb2 import State


logger = logging.getLogger(__name__)

class SampleServiceImpl(SampleServiceServicer):

    def CreateCall(self, request, context):
        logger.info("SampleServiceImpl.CreateCall")
        # do stateless validation
        StatelessValidation.validate(request)
        # send to chief of state, get resulting state
        result = CosClient.process_command(request.id, request)

        return self._handle_state_response(result, context)

    def AppendCall(self, request, context):
        logger.info("SampleServiceImpl.AppendCall")
        # do stateless validation
        StatelessValidation.validate(request)
        # send to chief of state, get resulting state
        try:
            result = CosClient.process_command(request.id, request)
            return self._handle_state_response(result, context)
        except Exception as e:
            # print(e.code())
            print("DETAILS ******")
            # print(e.details())
            # logger.error(f'cos failed, code=({e.code()}), details=({e.details()})')
            raise e

    def GetCall(self, request, context):
        logger.info("SampleServiceImpl.GetCall")
        # send to chief of state, get resulting state
        result = CosClient.get_state(request.id)
        return self._handle_state_response(result, context)

    @staticmethod
    def _handle_state_response(state, context):
        if state is None:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details("state was None")
            return State()
        else:
            return state
