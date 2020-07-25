# COS Python Sample App

Sample gRPC python application using [Chief of State](https://github.com/namely/chief-of-state).

### Overview

This sample application uses Chief of State to build [state](./proto/sample_app/state.proto) that
manages an array of strings and accepts [requests](./proto/sample_app/api.proto) to append more strings. State is derived from
[events](./proto/sample_app/events.proto).

### Quickstart

```bash
# updates submodules, generates protobufs
make setup

# starts all containers
make up

# see containers
make ps

# supervise logs
make logs

# run sample commands
make test
```
