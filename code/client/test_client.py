from test.test_api import TestApi
from test.test_handler import TestHandler
from test.test_cos import TestCos
import os

if __name__ == '__main__':

    # write_handler_host = os.environ.get("WRITE_HANDLER_HOST") or "write-handler"
    # write_handler_port = os.environ.get("WRITE_HANDLER_PORT") or "9011"
    # TestHandler.run(host = write_handler_host, port = write_handler_port)

    # cos_host = os.environ.get("COS_HOST") or "chiefofstate"
    # cos_port = os.environ.get("COS_PORT") or "9000"
    # TestCos.run(host = cos_host, port = cos_port)

    api_host = os.environ.get("API_HOST") or "api"
    api_port = os.environ.get("API_PORT") or "9010"
    TestApi.run(host = api_host, port = api_port)
