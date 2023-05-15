
.PHONY: help
.DEFAULT_GOAL := help

help: ## get a list of all the targets, and their short descriptions
	@# source for the incantation: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

backend: ## deploy the Q&A FastAPI backend service
	python3 api.py

prod_env: ## installs all required environment for production
	pip install -r requirements.txt

dev_env: ## installs all required environment for development
	pip install -r requirements-dev.txt

frontend: ## run streamlit with basic frontend page
	streamlit run forntend.py
