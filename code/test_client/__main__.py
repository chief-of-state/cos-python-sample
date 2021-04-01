from test_client.test_handler import TestHandler
from test_client.test_cos import TestCos
from test_client.test_api import TestApi
from shared.logging import configure_logging
from shared.grpc import get_tracer
import logging
import os

if __name__ == '__main__':

    configure_logging()

    tracer = get_tracer('test-client')

    logger = logging.getLogger("main")

    write_handler_host = os.environ.get("WRITE_HANDLER_HOST") or "write-handler"
    write_handler_port = os.environ.get("WRITE_HANDLER_PORT")

    cos_host = os.environ.get("COS_HOST") or "chiefofstate"
    cos_port = os.environ.get("COS_PORT")

    api_host = os.environ.get("API_HOST") or "api"
    api_port = os.environ.get("API_PORT")

    logger.info("BEGIN TESTS")

    TestHandler.run(host = write_handler_host, port = write_handler_port)
    TestCos.run(host = cos_host, port = cos_port)
    TestApi.run(host = api_host, port = api_port)

    logger.info("END TESTS")
