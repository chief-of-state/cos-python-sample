import os
import grpc
import logging
from concurrent import futures
from shared.logging import configure_logging
from banking_app_impl.service import BankingServiceImpl
from banking_app.api_pb2_grpc import add_BankAccountServiceServicer_to_server as register


def run(port):
    configure_logging()
    # define grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add grpc implementation to server
    register(BankingServiceImpl(), server)
    # set port
    server.add_insecure_port(f'[::]:{port}')
    # start
    server.start()
    logging.info(f"started server, {port}")
    server.wait_for_termination()
    logging.info("killing server")

if __name__ == '__main__':
    PORT = os.environ.get("APP_PORT") or "9000"
    run(PORT)
