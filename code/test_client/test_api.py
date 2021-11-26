from google.protobuf.empty_pb2 import Empty
from uuid import uuid4
import logging
import grpc
from grpc import StatusCode, RpcError
from grpc_status import rpc_status
from google.rpc import code_pb2, status_pb2, error_details_pb2

from banking_app.api_pb2_grpc import BankAccountServiceStub
from banking_app.api_pb2 import *
from banking_app.state_pb2 import BankAccount

from shared.grpc import get_channel
from shared.proto import *

logger = logging.getLogger("banking-app")

class TestApi():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port, True)
        stub = BankAccountServiceStub(channel)

        # TestApi._consistent_account(stub)

        # TestApi._missing_account(stub)
        # TestApi._missing_owner_rich_error(stub)

        # TestApi._validation_fail(stub)
        # TestApi._not_found(stub)
        # TestApi._rpc_fail(stub)
        # TestApi._no_op(stub)

        # create and do transactions against many accounts
        balances = {}
        num_accounts = 10

        for _ in range(num_accounts):
            id = TestApi._open(stub)
            balances[id] = 200

        for id in balances.keys():
            TestApi._debit(stub, id, balances)

        for id in balances.keys():
            TestApi._credit(stub, id, balances)

        for id in balances.keys():
            TestApi._get(stub, id, balances)

    @staticmethod
    def _get(stub: BankAccountServiceStub, id, balances):
        logger.info(f"checking balance {id}")
        response = stub.Get(GetAccountRequest(account_id=id))
        balance = response.account.account_balance
        assert balance == balances.get(id,0)

    @staticmethod
    def _open(stub: BankAccountServiceStub):
        account_owner = "random owner"
        cmd = OpenAccountRequest(account_owner=account_owner, balance=200)
        response = stub.OpenAccount(cmd)
        assert isinstance(response, ApiResponse)
        account_id = response.account.account_id
        logger.info(f"created account {account_id}")
        return account_id

    @staticmethod
    def _debit(stub: BankAccountServiceStub, id, balances):
        logger.info(f"debit account {id}")
        prior_balance = balances[id]
        request = DebitAccountRequest(account_id=id, amount=1)
        response = stub.DebitAccount(request)
        assert isinstance(response, ApiResponse)
        assert response.account.account_id==id
        assert response.account.account_balance == prior_balance - 1
        balances[id] = response.account.account_balance

    @staticmethod
    def _credit(stub: BankAccountServiceStub, id, balances):
        logger.info(f"credit account {id}")
        prior_balance = balances[id]
        request = CreditAccountRequest(account_id=id, amount=1)
        response = stub.CreditAccount(request)
        assert isinstance(response, ApiResponse)
        assert response.account.account_id==id
        assert response.account.account_balance == prior_balance + 1
        balances[id] = response.account.account_balance

    @staticmethod
    def _consistent_account(stub: BankAccountServiceStub):
        logger.info("test consistent account")
        id = '6ff6f770-7ab4-4161-b7f2-7aff57357065'

        try:
            # lazily create the account, ignore if already exists
            cmd = OpenAccountRequest(
                account_owner="consistent owner",
                balance=200,
                account_id=id
            )
            stub.OpenAccount(cmd)
            logger.info(f"created consistent account {id}")
        except RpcError as e:
            assert e.code() == StatusCode.ALREADY_EXISTS, f"wrong status code {e.code()}"
            logger.info(f"found consistent account {id}")

        request = DebitAccountRequest(account_id=id, amount=1)
        response = stub.DebitAccount(request)
        assert isinstance(response, ApiResponse)
        assert response.account.account_id==id, f"wrong ID '{response.account.account_id}'"
        logger.info(f"debitted consistent account {id}, balance {response.account.account_balance}")

    @staticmethod
    def _missing_owner_rich_error(stub: BankAccountServiceStub):
        logger.info("missing account owner, rich error")
        # open account request missing the owner
        cmd = OpenAccountRequest(balance=200)
        did_fail = False
        try:
            stub.OpenAccount(cmd)
        except RpcError as e:
            error_status = rpc_status.from_call(e)
            assert error_status.details, 'missing details'
            bad_request = unpack_any(error_status.details[0], error_details_pb2.BadRequest)
            assert bad_request.field_violations, 'missing violations'
            violation = bad_request.field_violations[0]
            assert violation.field == "account_owner"
            assert violation.description == "missing account owner"
            did_fail = True

        assert did_fail, "did not fail"

    @staticmethod
    def _missing_account(stub: BankAccountServiceStub):
        logger.info("test missing account")

        request = CreditAccountRequest(account_id=str(uuid4()))
        did_fail = False

        try:
            stub.CreditAccount(request)

        except RpcError as e:
            did_fail = True
            assert "account not found" in e.details().lower(), f"wrong error, {e.details()}"

        assert did_fail, "did not fail"

    @staticmethod
    def _validation_fail(stub: BankAccountServiceStub):
        logger.info("test validation failure")
        did_fail = False
        request = DebitAccountRequest(account_id=str(uuid4()), amount=-1) # will throw
        try:
            stub.DebitAccount(request)
        except grpc.RpcError as e:
            did_fail = True
            assert "amount must be greater than 0" in e.details().lower(), f'wrong error {e.details()}'
        assert did_fail, 'did not fail'

    @staticmethod
    def _rpc_fail(stub: BankAccountServiceStub):
        logger.info("test rpc failure")
        did_fail = False
        request = DebitAccountRequest(account_id=str(uuid4()), amount=1)
        try:
            stub.DebitAccount(request)
        except grpc.RpcError as e:
            did_fail = True
            assert e.code() == grpc.StatusCode.NOT_FOUND, e
            assert "account not found" in e.details().lower(), f'wrong error {e.details()}'
        assert did_fail, 'did not fail'

    @staticmethod
    def _not_found(stub):
        logger.info("test not found")
        did_fail = False
        request = GetAccountRequest(account_id=str(uuid4()))

        try:
            response = stub.Get(request)
            logger.info(type(response))
        except RpcError as e:
            assert e.code() == StatusCode.NOT_FOUND, "wrong status code"
            did_fail=True

        assert did_fail, 'did not fail'

    @staticmethod
    def _no_op(stub):

        logger.info("test no-op")
        # create account
        account_owner = "random owner"
        cmd = OpenAccountRequest(account_owner=account_owner, balance=200)
        response = stub.OpenAccount(cmd)
        assert isinstance(response, ApiResponse)
        account_id = response.account.account_id
        logger.info(f"hit {response.account.account_id}")
        balance = response.account.account_balance

        # apply $0 credit, which internally is a no-op command
        credit_response = stub.CreditAccount(CreditAccountRequest(
            account_id=account_id,
            amount=0
        ))

        assert credit_response.account.account_balance == balance
