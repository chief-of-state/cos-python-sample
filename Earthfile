FROM python:3.7-slim-stretch

all:
    BUILD +build-package

build-base:
    USER root

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install -r requirements.txt
    RUN rm -rf requirements.txt

    COPY -dir +protogen/chief_of_state .
    COPY -dir +protogen/banking_app .

    COPY -dir code/shared .

    SAVE IMAGE

build-package:
    FROM +build-base

    ARG VERSION=dev

    WORKDIR /app

    COPY -dir \
        code/read_handler_impl \
        code/write_handler_impl \
        code/banking_app_impl \
        code/test_client \
        .

    SAVE IMAGE cos-python-sample:${VERSION}

protogen:
    RUN pip install grpcio-tools

    RUN mkdir -p /defs
    RUN mkdir -p /gen

    WORKDIR /defs

    COPY -dir ./proto/chief-of-state-protos/chief_of_state /defs
    COPY -dir ./proto/local/banking_app /defs

    RUN ls -la /defs

    ARG SHARED_ARGS="-m grpc_tools.protoc -I/defs --python_out=/gen --grpc_python_out=/gen"
    RUN python ${SHARED_ARGS} /defs/chief_of_state/v1/*.proto
    RUN python ${SHARED_ARGS} /defs/banking_app/*.proto

    SAVE ARTIFACT /gen/chief_of_state AS LOCAL code/chief_of_state
    SAVE ARTIFACT /gen/banking_app AS LOCAL code/banking_app
