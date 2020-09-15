from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, CreateRequest
from sample_app.events_pb2 import AppendEvent, CreateEvent
from sample_app.state_pb2 import State
from chief_of_state.v1.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.v1.service_pb2 import ProcessCommandRequest, GetStateRequest
from shared.proto import ProtoHelper
from shared.grpc import get_channel
from uuid import uuid4
from grpc import StatusCode
from google.protobuf.empty_pb2 import Empty


class TestCos():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = ChiefOfStateServiceStub(channel)

        TestCos._test_noop(stub)

        id = uuid4().hex
        TestCos._test_create(stub, id)
        TestCos._test_append(stub, id)
        TestCos._test_fail_append(stub)
        TestCos._test_fail_id(stub)
        TestCos._test_fail_get(stub)

    @staticmethod
    def _test_noop(stub):
        print("TestCos.NoOp")
        id = uuid4().hex
        # create a command
        command = AppendRequest(id = id, append = 'no-op')
        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_id = id,
            command = ProtoHelper.pack_any(command)
        )
        # send to COS
        response = stub.ProcessCommand(cos_request)
        assert 'google.protobuf.Empty' in response.state.type_url, "expecting an empty!"

    @staticmethod
    def _test_create(stub, id):
        print("TestCos.CreateRequest")
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

    @staticmethod
    def _test_append(stub, id):
        print("TestCos.AppendRequest")

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

        assert output_state.id == id, output_state
        assert output_state.values == ['new'], output_state.values

    @staticmethod
    def _test_fail_append(stub):
        print("TestCos.fail_append")
        did_fail = False

        # create a command
        id = uuid4().hex
        command = AppendRequest(id = id)

        # wrap in COS request
        try:
            stub.ProcessCommand(
                ProcessCommandRequest(
                    entity_id=id,
                    command=ProtoHelper.pack_any(command)
                )
            )

        except Exception as e:
            did_fail = True
            assert 'cannot append empty value' in e.details().lower()

        assert did_fail

    @staticmethod
    def _test_fail_id(stub):
        print("TestCos.fail_id")
        did_fail = False

        # create a command
        id = ""
        command = AppendRequest(id = id, append="x")

        # wrap in COS request
        try:
            stub.ProcessCommand(
                ProcessCommandRequest(
                    entity_id=id,
                    command=ProtoHelper.pack_any(command)
                )
            )

        except Exception as e:
            did_fail = True
            assert 'empty entity id' in e.details().lower()

        assert did_fail


    @staticmethod
    def _test_fail_get(stub):
        print("TestCos.fail_get")
        did_fail = False

        # create a command
        command = GetStateRequest(entity_id="not-an-id")

        # wrap in COS request
        try:
            stub.GetState(command)

        except Exception as e:
            did_fail = True
            assert e.code() == StatusCode.NOT_FOUND, f'wrong error code, {e.code()}'

        assert did_fail

if __name__ == '__main__':
    TestCos.run()
