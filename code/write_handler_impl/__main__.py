from write_handler_impl.service import WriteSideHandlerImpl
from chief_of_state.v1.writeside_pb2_grpc import add_WriteSideHandlerServiceServicer_to_server
from shared.logging import configure_logging
import os
import logging
import grpc
from concurrent import futures


def run(port):
    configure_logging()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WriteSideHandlerServiceServicer_to_server(WriteSideHandlerImpl(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"started server, {port}")
    server.wait_for_termination()
    logging.info("killing server")

if __name__ == '__main__':
    PORT = os.environ.get("APP_PORT") or "9000"
    run(PORT)
