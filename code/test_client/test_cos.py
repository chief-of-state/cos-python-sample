from uuid import uuid4
from grpc import StatusCode
from google.protobuf.empty_pb2 import Empty
import logging

from banking_app.api_pb2_grpc import BankAccountServiceStub
from banking_app.api_pb2 import *
from banking_app.events_pb2 import *
from banking_app.state_pb2 import *

from chief_of_state.v1.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.v1.service_pb2 import ProcessCommandRequest, GetStateRequest
from chief_of_state.plugins.persisted_headers.v1.headers_pb2 import Headers, Header

from shared.proto import *
from shared.grpc import *

logger = logging.getLogger("chief-of-state")

class TestCos():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port, True)

        stub = ChiefOfStateServiceStub(channel)

        TestCos._fail(stub)

        # test general
        TestCos._persist_header(stub)
        TestCos._no_op(stub)
        TestCos._bad_request(stub)
        TestCos._bad_request_2(stub)
        TestCos._not_found(stub)

        channel.close()

    @staticmethod
    def _persist_header(stub):
        # persisted header is returned in the meta
        logger.info("persist header")
        id = str(uuid4())
        # create a command
        command = OpenAccountRequest(account_owner="some owner", balance=200)
        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_id = id,
            command = pack_any(command)
        )
        # send to COS
        meta_key = "x-custom-request-uuid"
        meta_value = str(uuid4)
        metadata = [(meta_key, meta_value)]
        # response = stub.ProcessCommand(request=cos_request, metadata=metadata)

        response, call = stub.ProcessCommand.with_call(request=cos_request, metadata=metadata)

        output_state = unpack_any(response.state, BankAccount)

        persisted_headers = response.meta.data.get("persisted_headers.v1")

        assert persisted_headers is not None, "missing persisted_headers.v1"
        persisted_headers = unpack_any(persisted_headers, Headers)
        header = persisted_headers.headers[0]
        assert header.key == meta_key, f"missing key {meta_key}"
        assert header.string_value == meta_value, f"missing key {meta_value}"


    @staticmethod
    def _no_op(stub):
        logger.info("no-op")
        id = str(uuid4())
        # create a command
        command = GetAccountRequest(account_id=id)
        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_id = id,
            command = pack_any(command)
        )
        # send to COS
        response = stub.ProcessCommand(cos_request)
        # get back a google.protobuf.Empty
        unpack_any(response.state, Empty)

    @staticmethod
    def _create(stub, id):
        logger.info("create state")
        # create a command
        command = OpenAccountRequest(account_owner="some owner", balance=200)

        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_id = id,
            command = pack_any(command)
        )

        # send to COS
        response = stub.ProcessCommand(cos_request)
        assert response.meta.revision_number == 1

        output_state = unpack_any(response.state, BankAccount)
        assert output_state.account_id == id
        assert output_state.account_balance == 200
        assert output_state.account_owner == "some owner"

    @staticmethod
    def _get(stub, id):
        logger.info("get state")

        # create a command
        command = GetStateRequest(entity_id=id)

        response = stub.GetState(command)
        output_state = unpack_any(response.state, BankAccount)
        assert output_state.account_id == id

    @staticmethod
    def _update(stub, id):
        logger.info("update state")

        # create a command
        command = DebitAccountRequest(amount=1)

        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_id = id,
            command = pack_any(command)
        )

        # send to COS
        response = stub.ProcessCommand(cos_request)
        assert response.meta.revision_number == 2

        output_state = unpack_any(response.state, BankAccount)

        assert output_state.account_id == id, output_state
        assert output_state.account_balance == 199


    @staticmethod
    def _fail(stub):
        logger.info("fail command")
        did_fail = False

        command = DebitAccountRequest(amount=999)

        # wrap in COS request
        try:
            stub.ProcessCommand(
                ProcessCommandRequest(
                    entity_id=str(uuid4()),
                    command=pack_any(command)
                )
            )

        except Exception as e:
            did_fail = True
            assert 'account not found' in e.details().lower()

        assert did_fail

    @staticmethod
    def _bad_request(stub):
        logger.info("bad request (validation)")
        did_fail = False

        # wrap in COS request
        try:
            stub.ProcessCommand(
                ProcessCommandRequest(
                    entity_id="",
                    command=pack_any(Empty())
                )
            )

        except grpc.RpcError as e:
            did_fail = True
            assert e.code() == StatusCode.INVALID_ARGUMENT
            assert 'empty entity id' in e.details().lower()

        assert did_fail

    @staticmethod
    def _bad_request_2(stub):
        logger.info("bad request (not found)")
        did_fail = False

        command = DebitAccountRequest(amount=999)

        # wrap in COS request
        try:
            stub.ProcessCommand(
                ProcessCommandRequest(
                    entity_id=str(uuid4()),
                    command=pack_any(command)
                )
            )

        except grpc.RpcError as e:
            did_fail = True
            assert e.code() == StatusCode.NOT_FOUND

        assert did_fail


    @staticmethod
    def _not_found(stub):
        logger.info("not found")
        did_fail = False

        # create a command
        bad_id = str(uuid4())
        command = GetStateRequest(entity_id=bad_id)

        # wrap in COS request
        try:
            stub.GetState(command)

        except grpc.RpcError as e:
            did_fail = True
            assert e.code() == StatusCode.NOT_FOUND, f'wrong error code, {e.code()}'

        assert did_fail

if __name__ == '__main__':
    TestCos.run()
