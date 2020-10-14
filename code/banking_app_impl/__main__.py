import os
import grpc
import logging
from concurrent import futures
from shared.logging import configure_logging
from shared.grpc import ServerHelper, get_tracer, intercept_grpc_server
from banking_app_impl.service import BankingServiceImpl
from banking_app.api_pb2_grpc import add_BankAccountServiceServicer_to_server as register

def run(port):
    configure_logging()
    # define grpc server
    tracer = get_tracer('api')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = intercept_grpc_server(server, tracer)
    # add grpc implementation to server
    register(BankingServiceImpl(), server)
    # set port
    server.add_insecure_port(f'[::]:{port}')
    # start
    server.start()
    logging.info(f"started server, {port}")
    ServerHelper().await_termination()
    logging.info("killing server")
    time.sleep(2)
    tracer.close()
    time.sleep(2)

if __name__ == '__main__':
    PORT = os.environ.get("APP_PORT") or "9000"
    run(PORT)
