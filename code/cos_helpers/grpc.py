import grpc


def get_channel(host, port):
    return grpc.insecure_channel(f'{host}:{port}')
