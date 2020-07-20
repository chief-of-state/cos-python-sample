from sample_app_impl.service import SampleServiceImpl
from cos_helpers.logging import configure_logging
from sample_app.api_pb2_grpc import add_SampleServiceServicer_to_server
import os
import logging
import grpc
from concurrent import futures


def run(port):
    configure_logging()
    logging.info("starting server")
    # define grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add grpc implementation to server
    add_SampleServiceServicer_to_server(SampleServiceImpl(), server)
    # set port
    server.add_insecure_port(f'[::]:{port}')
    # start
    server.start()
    server.wait_for_termination()
    logging.info("killing server")

if __name__ == '__main__':
    PORT = os.environ.get("APP_PORT") or "9010"
    run(PORT)
