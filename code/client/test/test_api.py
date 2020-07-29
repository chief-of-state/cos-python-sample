from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from sample_app.state_pb2 import State
from cos_helpers.grpc import get_channel
from uuid import uuid4

class TestApi():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = SampleServiceStub(channel)

        ids = [uuid4().hex for i in range(10)]

        for id in ids:
            TestApi.create(stub, id)

        for id in ids:
            TestApi.append(stub, id, str(uuid4().int))

        for id in ids:
            TestApi.get(stub, id)

        TestApi.api_failure(stub)
        TestApi.handler_validation_failure(stub)

    @staticmethod
    def create(stub, id):
        print("TestApi.create")
        request = CreateRequest(id = id)
        response = stub.CreateCall(request)
        assert isinstance(response, State)
        assert response.id == id


    @staticmethod
    def append(stub, id, value):
        print("TestApi.append")
        value = "y"
        request = AppendRequest(id = id, append = value)
        response = stub.AppendCall(request)
        assert isinstance(response, State)
        assert response.id == id
        assert value in response.values

    @staticmethod
    def get(stub, id):
        print("TestApi.get")
        request = GetRequest(id = id)
        response = stub.GetCall(request)
        assert isinstance(response, State)
        assert response.id == id

    @staticmethod
    def api_failure(stub):
        print("TestApi.handler_failure_id")
        request = AppendRequest(id = "", append="value") # will throw
        did_fail = False

        try:
            stub.AppendCall(request)
        except Exception as e:
            did_fail = True
            assert "empty entity id" in e.details().lower(), f"wrong error, {e.details()}"

        assert did_fail, "did not fail"

    @staticmethod
    def handler_validation_failure(stub):
        print("TestApi.handler_failure")
        did_fail = False
        request = AppendRequest(id = "x") # will throw
        try:
            stub.AppendCall(request)
        except Exception as e:
            did_fail = True
            assert "cannot append empty value" in e.details().lower(), f'wrong error {e.details()}'
        assert did_fail, 'did not fail'

if __name__ == '__main__':
    TestApi.run()
