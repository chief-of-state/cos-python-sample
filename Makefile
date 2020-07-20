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
	@ $(DCO) up -d test-client
	@ $(DCO) exec test-client bash

.phony: dco
dco:
	@echo $(DCO)

.phony: ps
ps:
	@ $(DCO) ps

.phony: logs
logs:
	@ $(DCO) logs -f --tail="all" api write-handler chiefofstate postgres

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
	@ $(DCO) restart -t 0 api write-handler
