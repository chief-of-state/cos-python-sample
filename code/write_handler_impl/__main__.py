from write_handler_impl.service import WriteSideHandlerImpl
from chief_of_state.v1.writeside_pb2_grpc import add_WriteSideHandlerServiceServicer_to_server
from shared.logging import configure_logging
from shared.grpc import ServerHelper, get_tracer, intercept_grpc_server
import os
import logging
import time
import grpc
from concurrent import futures

from jaeger_client import Config
import opentracing

def run(port):

    configure_logging()

    tracer = get_tracer('write-handler')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = intercept_grpc_server(server, tracer)

    add_WriteSideHandlerServiceServicer_to_server(WriteSideHandlerImpl(), server)

    server.add_insecure_port(f'[::]:{port}')
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
