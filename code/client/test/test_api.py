from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from sample_app.state_pb2 import State
from cos_helpers.grpc import get_channel

class TestApi():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = SampleServiceStub(channel)

        for i in range(0,10):
            id = f'some-id-{i}'
            TestApi.create(stub, id)
            TestApi.append(stub, id, i)
            TestApi.get(stub, id)

        # TestApi.create(stub, id)
        # TestApi.append(stub, id)
        # TestApi.get(stub, id)

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



if __name__ == '__main__':
    TestApi.run()
