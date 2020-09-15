import grpc
from grpc import StatusCode
from google.protobuf.message import Message

def get_channel(host, port):
    return grpc.insecure_channel(f'{host}:{port}')


def validate(condition, error_message:str = "", error_code:StatusCode = StatusCode.INVALID_ARGUMENT):
    '''validate or return error message'''
    fn = lambda context: condition or context.abort(code=error_code, details=error_message)
    return fn
