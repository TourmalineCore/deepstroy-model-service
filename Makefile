# If the first argument is "create-migration"...
ifeq (create-migration,$(firstword $(MAKECMDGOALS)))
ifeq ($(words $(MAKECMDGOALS)),2)
  # use the rest as arguments for "create-migration"
  $(info $(MAKECMDGOALS))
  MIGRATION_NAME := $(word 2,$(MAKECMDGOALS))

  ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(ARGS):;@true)
else
  $(error create-migration needs 1 argument. See help)
endif
endif

# help
###
.PHONY: help
help: ;@true
	$(info Makefile for Tourmanique project)
	$(info )
	$(info Avaliable targets: )
	$(info  * run                                       - runs the api locally via **docker**)
	$(info  * create-migration <migration_name>         - create migration with <migration_name> via **docker**)
	$(info )
	$(info Makefile: feel free to extend me!)


.PHONY: run
run: ## runs the api locally via **docker**
	docker compose -f docker-compose.yml up --build run-model-service

.PHONY: create-migration
create-migration: ## create migration with <migration_name> via **docker**
	docker compose -f docker-compose.yml run --rm --no-deps deepstroy-model-service poetry run flask db migrate -m "$(MIGRATION_NAME)"