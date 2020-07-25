from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, CreateRequest
from sample_app.events_pb2 import AppendEvent, CreateEvent
from sample_app.state_pb2 import State
from chief_of_state.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.service_pb2 import ProcessCommandRequest
from cos_helpers.proto import ProtoHelper
from cos_helpers.grpc import get_channel


class TestCos():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = ChiefOfStateServiceStub(channel)

        TestCos._test_create(stub)
        TestCos._test_append(stub)

    @staticmethod
    def _test_create(stub):
        print("TestCos.CreateRequest")

        id = "test-cos"
        # create a command
        command = CreateRequest(id = id)

        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_id = id,
            command = ProtoHelper.pack_any(command)
        )

        # send to COS
        response = stub.ProcessCommand(cos_request)

        output_state = ProtoHelper.unpack_any(response.state, State)
        assert output_state.id == id

    def _test_append(stub):
        print("TestCos.AppendRequest")

        id = "test-cos"
        # create a command
        command = AppendRequest(id = id, append = 'new')

        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_id = id,
            command = ProtoHelper.pack_any(command)
        )

        # send to COS
        response = stub.ProcessCommand(cos_request)

        output_state = ProtoHelper.unpack_any(response.state, State)
        assert output_state.id == id
        assert output_state.values == ['new']


if __name__ == '__main__':
    TestCos.run()
