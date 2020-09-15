import logging
from google.protobuf.any_pb2 import Any

from chief_of_state.v1.writeside_pb2 import HandleCommandRequest, HandleCommandResponse
from chief_of_state.v1.common_pb2 import MetaData

from shared.proto import unpack_any, get_field, pack_any, to_json
from shared.grpc import validate

from banking_app.state_pb2 import BankAccount
from banking_app.api_pb2 import *
from banking_app.events_pb2 import *


logger = logging.getLogger(__name__)

class CommandHandler():

    def __init__(self, context):
        self.context = context

    def handle_command(self, request: HandleCommandRequest):
        '''
        general command handler that matches on command type url
        and runs appropriate handler method
        '''
        logger.info(f"CommandHandler.handle_command")

        # unpack current state
        current_state: Any = get_field(request, "current_state")
        if current_state.type_url.endswith("google.protobuf.Empty"):
            current_state = BankAccount()
        else:
            current_state = unpack_any(current_state, BankAccount)

        if request.command.type_url.endswith('OpenAccountRequest'):
            command: OpenAccountRequest = unpack_any(request.command, OpenAccountRequest)
            return self._open_account(command, request.meta)

        elif request.command.type_url.endswith('DebitAccountRequest'):
            command: DebitAccountRequest = unpack_any(request.command, DebitAccountRequest)
            return self._debit_account(command, current_state, request.meta)

        elif request.command.type_url.endswith('CreditAccountRequest'):
            command: CreditAccountRequest = unpack_any(request.command, CreditAccountRequest)
            return self._credit_account(command, current_state, request.meta)

        elif request.command.type_url.endswith('GetAccountRequest'):
            return HandleCommandResponse()

        raise Exception(f"unknown type {request.command.type_url}")

    def _open_account(self, command: OpenAccountRequest, meta: MetaData):
        '''handle open account command'''

        # the first event results in revision 1, so it can expect revision 0 prior
        validate(meta.revision_number == 0, "account already exists")(self.context)

        event = AccountOpened(
            account_id=meta.entity_id,
            balance=command.balance,
            account_owner=command.account_owner
        )

        return HandleCommandResponse(event=pack_any(event))

    def _debit_account(self, command: DebitAccountRequest, current_state: BankAccount, meta: MetaData):
        '''handle debit'''
        validate(current_state is not None, "account not found")(self.context)
        validate(current_state.account_balance - command.amount >= 0, "insufficient funds")(self.context)

        event = AccountDebited(
            account_id=current_state.account_id,
            amount=command.amount
        )

        return HandleCommandResponse(event=pack_any(event))

    def _credit_account(self, command: CreditAccountRequest, current_state: BankAccount, meta: MetaData):
        '''handle credit'''
        validate(current_state is not None, "account not found")(self.context)

        event = AccountCredited(
            account_id=current_state.account_id,
            amount=command.amount
        )

        return HandleCommandResponse(event=pack_any(event))
