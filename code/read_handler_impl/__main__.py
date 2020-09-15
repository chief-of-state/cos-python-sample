import os
import logging
import grpc
from concurrent import futures
from read_handler_impl.service import ReadSideHandlerImpl
from chief_of_state.v1.readside_pb2_grpc import add_ReadSideHandlerServiceServicer_to_server as register
from shared.logging import configure_logging


def run(port):
    configure_logging()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    register(ReadSideHandlerImpl(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"started server, {port}")
    server.wait_for_termination()
    logging.info("killing server")

if __name__ == '__main__':
    PORT = os.environ.get("APP_PORT") or "9000"
    run(PORT)
