#   Makefile
#

.PHONY: all

-include Makefile.include

PACKAGE := sites-checker
REQ_FILE_TOOLS := requirements-tools.txt
STORAGE := ${HOME}/sites-storage
PYTHON3 := $(shell which python)
PIP3 := $(shell which pip)
PYV3 := $(shell $(PYTHON3) -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")

dockerfile = Dockerfile
module_name = $(MODULE_NAME)
EXPORT_VERSION = $(eval VERSION=$(shell cat .version))

.DEFAULT_GOAL : help

help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Clean
	@echo "======================================================"
	@echo clean $(PACKAGE)
	@echo "======================================================"
	rm -fR __pycache__ venv "*.pyc"
	find ./* -maxdepth 0 -name "*.pyc" -type f -delete

install-tools-requirements: ## install requirements of service
	@echo "======================================================"
	@echo "install-tools-requirements $(PYV3)"
	@echo "======================================================"
	pip3 install --upgrade pip
	pip3 install --upgrade -r $(REQ_FILE_TOOLS)

yapf: install-tools-requirements ## yapf
	@echo "======================================================"
	@echo yapf $(PACKAGE)
	@echo "======================================================"
	@$(PYTHON3) -m yapf --style .style.yapf --in-place . --recursive

pep8: install-tools-requirements ## pep8
	@echo "======================================================"
	@echo pep8 $(PACKAGE)
	@echo "======================================================"
	@$(PYTHON3) -m pep8 --config .pep8 .

run-infra: ## run-infra
	@docker-compose -f docker-compose.infra.yml up -d> /dev/null

set-configs: ## set configuration service
	@$(PYTHON3) ./Infra/scripts/set_consul_configs.py

run-service: ## run service
	@$(PYTHON3) ./Infra/scripts/run_service.py

stop-all:
	@docker-compose -f docker-compose.infra.yml -f docker-compose.prod.yml -f docker-compose.local.yml down> /dev/null

start-all:
	@docker-compose -f docker-compose.infra.yml -f docker-compose.prod.yml -f docker-compose.local.yml up -d> /dev/null

list: ## Makefile target list
	@echo "======================================================"
	@echo Makefile target list
	@echo "======================================================"
	@cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort
