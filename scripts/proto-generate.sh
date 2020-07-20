#!/bin/bash

pip install grpcio grpcio-tools

# SERVER

rm -rf ./code/server/sample_app/*pb2*.py
rm -rf ./code/server/chief_of_state/*pb2*.py

python -m grpc_tools.protoc \
    -I./proto/ \
    --python_out=./code/server/ \
    --grpc_python_out=./code/server/ \
    ./proto/sample_app/*.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./code/server/ \
    --grpc_python_out=./code/server/ \
    ./submodules/chief-of-state-protos/chief_of_state/writeside.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./code/server/ \
    --grpc_python_out=./code/server/ \
    ./submodules/chief-of-state-protos/chief_of_state/common.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./code/server/ \
    --grpc_python_out=./code/server/ \
    ./submodules/chief-of-state-protos/chief_of_state/service.proto


# CLIENT

rm -rf ./code/client/sample_app/
rm -rf ./code/client/chief_of_state/

python -m grpc_tools.protoc \
    -I./proto/ \
    --python_out=./code/client/ \
    --grpc_python_out=./code/client/ \
    ./proto/sample_app/*.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./code/client/ \
    --grpc_python_out=./code/client/ \
    ./submodules/chief-of-state-protos/chief_of_state/writeside.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./code/client/ \
    --grpc_python_out=./code/client/ \
    ./submodules/chief-of-state-protos/chief_of_state/common.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./code/client/ \
    --grpc_python_out=./code/client/ \
    ./submodules/chief-of-state-protos/chief_of_state/service.proto
