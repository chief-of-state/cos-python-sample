FROM python:3.7-slim-stretch

all:
    BUILD +build-package

build-base:
    USER root

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install -r requirements.txt
    RUN rm -rf requirements.txt

    COPY -dir +protogen/sample_app .
    COPY -dir +protogen/chief_of_state .

    COPY -dir code/cos_helpers .

    SAVE IMAGE

build-package:
    FROM +build-base

    ARG VERSION=dev

    WORKDIR /app

    COPY -dir \
        code/read_handler_impl \
        code/sample_app_impl \
        code/write_handler_impl \
        code/test \
        .

    SAVE IMAGE cos-python-sample:${VERSION}

protogen:
    RUN pip install grpcio-tools

    RUN mkdir -p /defs
    RUN mkdir -p /gen

    WORKDIR /defs

    COPY -dir ./proto/local/sample_app /defs
    COPY -dir ./proto/chief-of-state-protos/chief_of_state /defs

    RUN ls -la /defs

    ARG SHARED_ARGS="-m grpc_tools.protoc -I/defs --python_out=/gen --grpc_python_out=/gen"
    RUN python ${SHARED_ARGS} /defs/sample_app/*.proto
    RUN python ${SHARED_ARGS} /defs/chief_of_state/v1/*.proto

    SAVE ARTIFACT /gen/sample_app AS LOCAL code/sample_app
    SAVE ARTIFACT /gen/chief_of_state AS LOCAL code/chief_of_state
