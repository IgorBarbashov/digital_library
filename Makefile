SHELL := /bin/bash
COMPOSE := docker compose
ENV_FILE := .env

.PHONY: help env build up-dev up-prod down logs ps shell restart

help:
	@echo "Makefile targets:"
	@echo "  make env        # copy .env.example -> .env if not present"
	@echo "  make build      # build images (uses docker compose)"
	@echo "  make up-dev     # start dev (mounts source, reload)"
	@echo "  make up-prod    # start production (detached)"
	@echo "  make down       # stop and remove containers + volumes"
	@echo "  make logs       # follow logs"
	@echo "  make ps         # show containers"
	@echo "  make shell      # open a shell in the web container"
	@echo "  make restart    # restart production (down + up-prod)"

env:
	@if [ ! -f $(ENV_FILE) ]; then \
		cp .env.example $(ENV_FILE) && echo "Created $(ENV_FILE) from .env.example"; \
	else \
		echo "$(ENV_FILE) already exists"; \
	fi

build: env
	$(COMPOSE) -f docker-compose.yml build --pull --no-cache

up-dev: env
	$(COMPOSE) -f docker-compose.yml -f docker-compose.override.yml up --build

up-prod: env
	$(COMPOSE) -f docker-compose.yml up --build -d

down:
	$(COMPOSE) -f docker-compose.yml down --volumes --remove-orphans

logs:
	$(COMPOSE) -f docker-compose.yml logs -f --tail=200

ps:
	$(COMPOSE) -f docker-compose.yml ps

shell:
	@echo "Opening shell in web container (service: web)"
	$(COMPOSE) exec web /bin/bash || $(COMPOSE) exec web sh

restart: down up-prod
