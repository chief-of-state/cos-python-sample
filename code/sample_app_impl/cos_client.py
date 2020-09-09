import os
import logging
from chief_of_state.v1.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.v1.service_pb2 import ProcessCommandRequest, GetStateRequest
from cos_helpers.proto import ProtoHelper
from cos_helpers.grpc import get_channel
from sample_app.state_pb2 import State
from google.protobuf.empty_pb2 import Empty
from google.protobuf.any_pb2 import Any

logger = logging.getLogger(__name__)

class CosClient():

    @staticmethod
    def get_state(id):
        logger.debug('begin get_state')
        client = CosClient._get_cos_client()
        command = GetStateRequest(entity_id=id)
        response = client.GetState(command)
        return CosClient.optional_state(response.state)

    @staticmethod
    def process_command(id, command):
        logger.debug("begin process_command")
        client = CosClient._get_cos_client()
        command_any = ProtoHelper.pack_any(command)
        request = ProcessCommandRequest(entity_id=id, command=command_any)
        response = client.ProcessCommand(request)
        return CosClient.optional_state(response.state)

    @staticmethod
    def _get_cos_client():
        host = os.environ.get("COS_HOST")
        port = os.environ.get("COS_PORT")
        channel = get_channel(host, port)
        return ChiefOfStateServiceStub(channel)

    @staticmethod
    def optional_state(any_state):
        '''return state or None if a proto Empty message'''
        assert isinstance(any_state, Any), 'expecting Any'

        if any_state.type_url.endswith('google.protobuf.Empty'):
            logger.debug('converting google.protobuf.Empty to None')
            return None
        else:
            return ProtoHelper.unpack_any(any_state, State)
