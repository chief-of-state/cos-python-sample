# COS Python Sample App

Sample gRPC python application using [Chief of State](https://github.com/namely/chief-of-state).

### Overview

This sample application uses Chief of State to build [state](./proto/sample_app/state.proto) that
manages an array of strings and accepts [requests](./proto/sample_app/api.proto) to append more strings. State is derived from
[events](./proto/sample_app/events.proto).

### Quickstart

```bash
# download earth
brew install earthly

# updates submodules, generates protobufs
earth +all

# starts all containers
docker-compose up -d

# see containers
docker-compose ps

# run sample commands
docker-compose exec test-client python -m test

# supervise app logs
docker-compose logs -f --tail="all" api write-handler read-handler

# cos logs
docker-compose logs -f chiefofstate
```
