import grpc
import logging
from uuid import uuid4
from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty

from banking_app.api_pb2 import *
from banking_app.events_pb2 import *
from banking_app.state_pb2 import BankAccount

from chief_of_state.v1.writeside_pb2_grpc import WriteSideHandlerServiceStub
from chief_of_state.v1.writeside_pb2 import *
from chief_of_state.v1.common_pb2 import MetaData

from shared.grpc import get_channel
from shared.proto import *


logger = logging.getLogger('write-handler')

class TestHandler():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = WriteSideHandlerServiceStub(channel)

        Commands._open(stub)
        Commands._debit(stub)
        Commands._credit(stub)
        Commands._bad_request(stub)

class Commands():
    @staticmethod
    def _open(stub):
        logger.info("open account")

        account_owner = "random owner"
        cmd = OpenAccountRequest(account_owner=account_owner, balance=200)

        request = HandleCommandRequest(
            command=pack_any(cmd),
            prior_state=pack_any(Empty()),
            prior_event_meta=MetaData(),
        )

        response = stub.HandleCommand(request)

        assert isinstance(response, HandleCommandResponse)

        response_event = unpack_any(response.event, AccountOpened)

        assert response_event.balance == 200
        assert response_event.account_owner == account_owner

    @staticmethod
    def _debit(stub):
        logger.info("debit account")

        id = str(uuid4())

        command = DebitAccountRequest(account_id=id, amount=1)
        prior_state = BankAccount(
            account_id=id,
            account_balance=100,
            account_owner="some owner"
        )
        meta = MetaData(revision_number=1)

        request = HandleCommandRequest(
            command=pack_any(command),
            prior_state=pack_any(prior_state),
            prior_event_meta=meta
        )

        response = stub.HandleCommand(request)

        assert isinstance(response, HandleCommandResponse)

        response_event = unpack_any(response.event, AccountDebited)

        assert response_event.amount == 1

    @staticmethod
    def _credit(stub):
        logger.info("credit account")

        id = str(uuid4())

        command = CreditAccountRequest(account_id=id, amount=1)
        prior_state = BankAccount(
            account_id=id,
            account_balance=100,
            account_owner="some owner"
        )
        meta = MetaData(revision_number=1)

        request = HandleCommandRequest(
            command=pack_any(command),
            prior_state=pack_any(prior_state),
            prior_event_meta=meta
        )

        response = stub.HandleCommand(request)

        assert isinstance(response, HandleCommandResponse)

        response_event = unpack_any(response.event, AccountCredited)

        assert response_event.amount == 1

    @staticmethod
    def _bad_request(stub):
        logger.info("simulate bad request")

        # try to debit with no money!
        cmd = DebitAccountRequest(amount=1)
        state = BankAccount(account_balance=0)

        request = HandleCommandRequest(
            command=pack_any(cmd),
            prior_state=pack_any(state),
            prior_event_meta=MetaData(),
        )

        did_fail = False

        try:
            stub.HandleCommand(request)
        except grpc.RpcError as e:
            did_fail = True
            assert e.code() == grpc.StatusCode.INVALID_ARGUMENT, e
            assert e.details() == "account not found", e.details()

        assert did_fail, "supposed to fail!"

if __name__ == '__main__':
    TestApi.run()
