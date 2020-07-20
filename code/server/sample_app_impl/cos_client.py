import os
import logging
from chief_of_state.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.service_pb2 import ProcessCommandRequest
from cos_helpers.proto import ProtoHelper
from cos_helpers.grpc import get_channel
from sample_app.state_pb2 import State


logger = logging.getLogger(__name__)

class CosClient():

    @staticmethod
    def process_command(id, command):
        logger.debug("begin process_command")

        command_any = ProtoHelper.pack_any(command)

        cos_request = ProcessCommandRequest(
            entity_uuid = id,
            command = command_any
        )

        stub = CosClient._get_cos_stub()

        try:
            response = stub.ProcessCommand(cos_request)
            resulting_state = ProtoHelper.unpack_any(response.state, State)
            return resulting_state

        except Exception as e:
            logger.error("CosClient call failed", e)
            raise e

    @staticmethod
    def _get_cos_stub():
        host = os.environ.get("COS_HOST")
        port = os.environ.get("COS_PORT")
        channel = get_channel(host, port)
        return ChiefOfStateServiceStub(channel)
