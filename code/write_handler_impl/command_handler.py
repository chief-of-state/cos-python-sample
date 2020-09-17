import logging
from google.protobuf.any_pb2 import Any
from grpc import StatusCode

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

        self.command_router = {
            'OpenAccountRequest': self._open_account,
            'DebitAccountRequest': self._debit_account,
            'CreditAccountRequest': self._credit_account,
            'GetAccountRequest': self._no_op
        }


    def handle_command(self, request: HandleCommandRequest):
        '''
        general command handler that matches on command type url
        and runs appropriate handler method
        '''

        # unpack current state
        current_state = None

        current_state_any: Any = get_field(request, "current_state")
        validate(current_state_any is not None, error_code=StatusCode.INTERNAL)(self.context)

        if not current_state_any.type_url.endswith("google.protobuf.Empty"):
            current_state = unpack_any(current_state_any, BankAccount)

        # get the handler by type url
        handler_key = request.command.type_url.split('.')[-1]
        logger.info(f"handling command {handler_key}")

        handler = self.command_router.get(handler_key)

        if not handler:
            raise Exception(f"unknown type {request.command.type_url}")

        return handler(request, current_state, request.meta)

    def _open_account(self, request: HandleCommandRequest, current_state: BankAccount, meta: MetaData):
        '''handle open account command'''

        # the first event results in revision 1, so it can expect revision 0 prior
        validate(meta.revision_number == 0, "account already exists")(self.context)

        command: OpenAccountRequest = unpack_any(request.command, OpenAccountRequest)

        event = AccountOpened(
            account_id=meta.entity_id,
            balance=command.balance,
            account_owner=command.account_owner
        )

        return HandleCommandResponse(event=pack_any(event))

    def _debit_account(self, request: HandleCommandRequest, current_state: BankAccount, meta: MetaData):
        '''handle debit'''
        validate(meta.revision_number > 0, "account not found")(self.context)

        command: DebitAccountRequest = unpack_any(request.command, DebitAccountRequest)
        validate(current_state.account_balance - command.amount >= 0, "insufficient funds")(self.context)

        event = AccountDebited(
            account_id=current_state.account_id,
            amount=command.amount
        )

        return HandleCommandResponse(event=pack_any(event))

    def _credit_account(self, request: HandleCommandRequest, current_state: BankAccount, meta: MetaData):
        '''handle credit'''

        validate(meta.revision_number > 0, "account not found")(self.context)

        command: CreditAccountRequest = unpack_any(request.command, CreditAccountRequest)

        validate(command.amount >= 0, "credit must be positive")(self.context)

        # if crediting $0, return a no-op
        if command.amount == 0:
            return HandleCommandResponse()

        event = AccountCredited(
            account_id=current_state.account_id,
            amount=command.amount
        )

        return HandleCommandResponse(event=pack_any(event))

    def _no_op(self, *args, **kwargs):
        return HandleCommandResponse()
