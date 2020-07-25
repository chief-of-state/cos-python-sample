DCO := docker-compose --project-directory . -f ./docker/docker-compose.yml

.phony: setup
setup:
	@git submodule update --init
	@make protogen

.phony: protogen
protogen:
	@docker run \
		-v `pwd`:/mnt/local/ \
		-w /mnt/local/ \
		python:3.7.6-stretch \
		./scripts/proto-generate.sh

.phony: test-client
test-client:
	# @ $(DCO) exec test-client bash

.phony: test
test:
	@ $(DCO) exec test-client python ./test_client.py

.phony: dco
dco:
	@echo $(DCO)

.phony: ps
ps:
	@ $(DCO) ps

.phony: logs
logs:
	@ $(DCO) logs -f --tail="all" api write-handler read-handler chiefofstate postgres

.phony: logs-apps
logs-apps:
	@ $(DCO) logs -f --tail="all" api write-handler read-handler


.phony: build
build:
	@ $(DCO) build

.phony: up
up:
	@ $(DCO) up -d

.phony: down
down:
	@ $(DCO) down -t 0 --remove-orphans

.phony: restart
restart:
	@ $(DCO) stop -t 0 api write-handler read-handler
	@ $(DCO) rm -f api write-handler read-handler
	@ $(DCO) up -d api write-handler read-handler
