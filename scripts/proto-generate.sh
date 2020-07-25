#!/bin/bash

PROTO_DIR=${PROTO_DIR:-"./.generated/"}

echo "PROTO_DIR=$PROTO_DIR"

pip install grpcio grpcio-tools

rm -rf $PROTO_DIR
mkdir -p $PROTO_DIR

python -m grpc_tools.protoc \
    -I./proto/ \
    --python_out=$PROTO_DIR \
    --grpc_python_out=$PROTO_DIR \
    ./proto/sample_app/*.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=$PROTO_DIR \
    --grpc_python_out=$PROTO_DIR \
    ./submodules/chief-of-state-protos/chief_of_state/writeside.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=$PROTO_DIR \
    --grpc_python_out=$PROTO_DIR \
    ./submodules/chief-of-state-protos/chief_of_state/readside.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=$PROTO_DIR \
    --grpc_python_out=$PROTO_DIR \
    ./submodules/chief-of-state-protos/chief_of_state/common.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=$PROTO_DIR \
    --grpc_python_out=$PROTO_DIR \
    ./submodules/chief-of-state-protos/chief_of_state/service.proto
