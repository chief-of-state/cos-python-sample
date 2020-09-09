# COS Python Sample App

Sample gRPC python application using [Chief of State](https://github.com/namely/chief-of-state).

### Overview

This sample application uses Chief of State to build [state](./proto/local/sample_app/state.proto) that
manages an array of strings and accepts [requests](./proto/local/sample_app/api.proto) to append more strings. State is derived from
[events](./proto/local/sample_app/events.proto).

### Quickstart

```bash
# download earth
brew install earthly

# updates submodules, generates protobufs
earth +all

# starts all containers
docker-compose up -d

# run sample commands
docker-compose exec test-client python -m test

# OTHER HELPFUL COMMANDS

# only generate protobufs locally
earth +protogen

# supervise app logs
docker-compose logs -f --tail="all" api write-handler read-handler

# cos logs
docker-compose logs -f chiefofstate
```
