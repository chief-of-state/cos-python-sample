import logging
from google.protobuf.any_pb2 import Any
from chief_of_state.v1.writeside_pb2 import HandleEventRequest, HandleEventResponse
from chief_of_state.v1.common_pb2 import MetaData
from banking_app.state_pb2 import BankAccount
from banking_app.events_pb2 import *
from shared.proto import *


logger = logging.getLogger(__name__)

class EventHandler():
    @classmethod
    def handle_event(cls, request: HandleEventRequest):

        current_state = get_field(request, "current_state")
        if current_state.type_url.endswith("google.protobuf.Empty"):
            None
        else:
            current_state = unpack_any(current_state, BankAccount)

        if request.event.type_url.endswith("AccountOpened"):
            event = unpack_any(request.event, AccountOpened)
            return cls._handle_open(event)

        elif request.event.type_url.endswith("AccountDebited"):
            event = unpack_any(request.event, AccountDebited)
            return EventHandler._handle_debit(event, current_state)

        elif request.event.type_url.endswith("AccountCredited"):
            event = unpack_any(request.event, AccountCredited)
            return EventHandler._handle_credit(event, current_state)

        raise Exception(f'unhandled event {event.type_url}')

    @staticmethod
    def _handle_open(event: AccountOpened):
        '''handle account opened'''

        new_state = BankAccount(
            account_id = event.account_id,
            account_balance = event.balance,
            account_owner = event.account_owner,
            is_closed = False
        )

        # create return
        response = HandleEventResponse()
        response.resulting_state.CopyFrom(pack_any(new_state))
        return response

    def _handle_debit(event: AccountDebited, current_state: BankAccount):
        '''handle debit'''
        new_state = BankAccount()
        new_state.CopyFrom(current_state)
        new_state.account_balance -= event.amount
        # create return
        response = HandleEventResponse()
        response.resulting_state.CopyFrom(pack_any(new_state))
        return response


    def _handle_credit(event: AccountCredited, current_state: BankAccount):
        '''handle credit'''
        new_state = BankAccount()
        new_state.CopyFrom(current_state)
        new_state.account_balance += event.amount
        # create return
        response = HandleEventResponse()
        response.resulting_state.CopyFrom(pack_any(new_state))
        return response
