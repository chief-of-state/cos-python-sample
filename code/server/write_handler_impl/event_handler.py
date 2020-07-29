import logging
from sample_app.events_pb2 import AppendEvent, CreateEvent
from sample_app.state_pb2 import State
from chief_of_state.writeside_pb2 import HandleEventResponse
from cos_helpers.proto import ProtoHelper


logger = logging.getLogger(__name__)

class EventHandler():
    @staticmethod
    def handle_event(event, current_state, meta):
        if ('AppendEvent' in event.type_url):
            return EventHandler._handle_append(event, current_state, meta)

        elif ('CreateEvent' in event.type_url):
            return EventHandler._handle_create(event, current_state, meta)

        else:
            raise Exception(f'unhandled event {event.type_url}')


    def _handle_append(event, current_state, meta):
        real_current_state = ProtoHelper.unpack_any(current_state, State)
        real_event = ProtoHelper.unpack_any(event, AppendEvent)

        # build new state
        new_state = State()
        new_state.CopyFrom(real_current_state)
        new_state.id = real_event.id

        new_state.values.append(real_event.appended)

        # create return
        any_new_state = ProtoHelper.pack_any(new_state)

        response = HandleEventResponse()
        response.resulting_state.CopyFrom(any_new_state)

        return response


    def _handle_create(event, current_state, meta):
        real_event = ProtoHelper.unpack_any(event, CreateEvent)

        new_state = State(id = real_event.id)
        any_new_state = ProtoHelper.pack_any(new_state)

        response = HandleEventResponse()
        response.resulting_state.CopyFrom(any_new_state)

        return response
