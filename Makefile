.DEFAULT_GOAL := help

run: ## run main.py
	@echo "Starting bot"
	python main.py

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

migrate-create: ## Create a new migration
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply: ## Apply migrations
	alembic upgrade head

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

docs-generate: ## Generate HTML documentation for the entire project
	@echo "Generating documentation..."
	rm -rf docs_html
	pdoc bot_config database filters handlers keyboards models projects_images repository services setup templates --output-dir docs_html

docs-open: ## Open generated HTML documentation in browser
ifeq ($(OS),Windows_NT)
	@start docs_html\index.html
else
	@xdg-open docs_html/index.html || open docs_html/index.html
endif
