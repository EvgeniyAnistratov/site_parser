#!/usr/bin/make
# Makefile readme (ru): <http://linux.yaroslavl.ru/docs/prog/gnu_make_3-79_russian_manual.html>
# Makefile readme (en): <https://www.gnu.org/software/make/manual/html_node/index.html#SEC_Contents>

dc_bin := $(shell command -v docker-compose 2> /dev/null)

SHELL = /bin/sh
RUN_APP_ARGS = --rm --user "$(shell id -u):$(shell id -g)" app

.PHONY : help build shell test lint start shutdown restart logs clean
.DEFAULT_GOAL : help

# This will output the help for each task. thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build:
	$(dc_bin) build

shell: ## Start shell into container
	$(dc_bin) run $(RUN_APP_ARGS) sh

test: ## Execute tests
	$(dc_bin) run $(RUN_APP_ARGS) pytest

lint:
	$(dc_bin) run $(RUN_APP_ARGS) flake8 .

start: ## Start services
	$(dc_bin) up --detach

shutdown: ## Stop services
	$(dc_bin) down -t 5

restart: shutdown start ## Restart all containers

logs: ## Show logs
	$(dc_bin) logs -f app

clean:
	$(dc_bin) down -v
