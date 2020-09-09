import os
import logging
from chief_of_state.v1.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.v1.service_pb2 import ProcessCommandRequest, GetStateRequest
from cos_helpers.proto import ProtoHelper
from cos_helpers.grpc import get_channel
from sample_app.state_pb2 import State

logger = logging.getLogger(__name__)

class CosClient():

    @staticmethod
    def get_state(id):
        logger.debug('begin get_state')
        client = CosClient._get_cos_client()
        command = GetStateRequest(entity_id=id)
        response = client.GetState(command)
        resulting_state = ProtoHelper.unpack_any(response.state, State)
        return resulting_state

    @staticmethod
    def process_command(id, command):
        logger.debug("begin process_command")
        client = CosClient._get_cos_client()
        command_any = ProtoHelper.pack_any(command)
        request = ProcessCommandRequest(entity_id=id, command=command_any)
        response = client.ProcessCommand(request)
        resulting_state = ProtoHelper.unpack_any(response.state, State)
        return resulting_state

    @staticmethod
    def _get_cos_client():
        host = os.environ.get("COS_HOST")
        port = os.environ.get("COS_PORT")
        channel = get_channel(host, port)
        return ChiefOfStateServiceStub(channel)
