# Python Library Makefile
# Canonical Makefile for Python library projects in the provide.io ecosystem
# This file is maintained in provide-foundry and extracted to library projects
#
# Source: provide-foundry/src/provide/foundry/config/Makefile.python.tmpl
# Do not edit directly in library projects - changes will be overwritten
# To update: run `make update-makefile` or extract from provide-foundry

.PHONY: help setup test test-parallel test-verbose test-unit test-integration coverage lint lint-fix format format-check typecheck quality quality-all build clean install uninstall lock version dev-setup dev-test dev-check ci-test ci-quality ci-all docs-setup docs-build docs-serve docs-clean

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# ==============================================================================
# 📖 Help & Information
# ==============================================================================

help: ## Show this help message
	@echo '$(BLUE)Available targets:$(NC)'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ==============================================================================
# 🔧 Setup & Environment
# ==============================================================================

setup: ## Initialize development environment
	@echo '$(BLUE)Setting up development environment...$(NC)'
	uv sync
	@echo '$(GREEN)✓ Development environment ready$(NC)'

# ==============================================================================
# 🧪 Testing
# ==============================================================================

test: ## Run all tests
	@echo '$(BLUE)Running tests...$(NC)'
	uv run pytest
	@echo '$(GREEN)✓ Tests complete$(NC)'

test-parallel: ## Run tests in parallel
	@echo '$(BLUE)Running tests in parallel...$(NC)'
	uv run pytest -n auto
	@echo '$(GREEN)✓ Tests complete$(NC)'

test-verbose: ## Run tests with verbose output
	@echo '$(BLUE)Running tests with verbose output...$(NC)'
	uv run pytest -vvv
	@echo '$(GREEN)✓ Tests complete$(NC)'

test-unit: ## Run only unit tests
	@echo '$(BLUE)Running unit tests...$(NC)'
	uv run pytest -m unit
	@echo '$(GREEN)✓ Unit tests complete$(NC)'

test-integration: ## Run only integration tests
	@echo '$(BLUE)Running integration tests...$(NC)'
	uv run pytest -m integration
	@echo '$(GREEN)✓ Integration tests complete$(NC)'

coverage: ## Run tests with coverage report
	@echo '$(BLUE)Running tests with coverage...$(NC)'
	uv run pytest --cov=src --cov-report=html --cov-report=term
	@echo '$(GREEN)✓ Coverage report generated in htmlcov/$(NC)'

# ==============================================================================
# 🔍 Code Quality
# ==============================================================================

lint: ## Run linter (ruff check)
	@echo '$(BLUE)Running linter...$(NC)'
	uv run ruff check .
	@echo '$(GREEN)✓ Linting complete$(NC)'

lint-fix: ## Run linter with auto-fix
	@echo '$(BLUE)Running linter with auto-fix...$(NC)'
	uv run ruff check . --fix
	@echo '$(GREEN)✓ Linting complete$(NC)'

format: ## Format code with ruff
	@echo '$(BLUE)Formatting code...$(NC)'
	uv run ruff format .
	@echo '$(GREEN)✓ Code formatted$(NC)'

format-check: ## Check code formatting without modifying
	@echo '$(BLUE)Checking code formatting...$(NC)'
	uv run ruff format . --check
	@echo '$(GREEN)✓ Format check complete$(NC)'

typecheck: ## Run type checker (mypy)
	@echo '$(BLUE)Running type checker...$(NC)'
	uv run mypy src/
	@echo '$(GREEN)✓ Type checking complete$(NC)'

quality: lint typecheck ## Run all quality checks (lint + typecheck)
	@echo '$(GREEN)✓ All quality checks passed$(NC)'

quality-all: format-check lint typecheck test ## Run all quality checks including tests
	@echo '$(GREEN)✓ All quality checks and tests passed$(NC)'

# ==============================================================================
# 🏗️ Build & Package
# ==============================================================================

build: ## Build package
	@echo '$(BLUE)Building package...$(NC)'
	uv build
	@echo '$(GREEN)✓ Package built in dist/$(NC)'

# ==============================================================================
# 🧹 Clean
# ==============================================================================

clean: ## Clean build artifacts and caches
	@echo '$(BLUE)Cleaning build artifacts...$(NC)'
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .hypothesis
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo '$(GREEN)✓ Cleanup complete$(NC)'

# ==============================================================================
# 📦 Package Management
# ==============================================================================

install: ## Install package in development mode
	@echo '$(BLUE)Installing package in development mode...$(NC)'
	uv pip install -e .
	@echo '$(GREEN)✓ Package installed$(NC)'

uninstall: ## Uninstall package
	@echo '$(BLUE)Uninstalling package...$(NC)'
	uv pip uninstall -y $$(grep '^name = ' pyproject.toml | cut -d'"' -f2)
	@echo '$(GREEN)✓ Package uninstalled$(NC)'

lock: ## Update dependency lock file
	@echo '$(BLUE)Updating dependency lock file...$(NC)'
	uv lock
	@echo '$(GREEN)✓ Lock file updated$(NC)'

version: ## Show package version
	@echo '$(BLUE)Package version:$(NC)'
	@cat VERSION 2>/dev/null || grep '^version = ' pyproject.toml | cut -d'"' -f2

# ==============================================================================
# 🚀 Development Workflow Shortcuts
# ==============================================================================

dev-setup: setup ## Alias for setup
	@echo '$(GREEN)✓ Ready for development$(NC)'

dev-test: test-parallel ## Quick test run for development
	@echo '$(GREEN)✓ Development tests complete$(NC)'

dev-check: format lint typecheck ## Quick quality check for development
	@echo '$(GREEN)✓ Development checks complete$(NC)'

# ==============================================================================
# 🤖 CI/CD Targets
# ==============================================================================

ci-test: test-parallel coverage ## Run tests with coverage for CI
	@echo '$(GREEN)✓ CI tests complete$(NC)'

ci-quality: format-check lint typecheck ## Run all quality checks for CI
	@echo '$(GREEN)✓ CI quality checks complete$(NC)'

ci-all: ci-quality ci-test build ## Run full CI pipeline
	@echo '$(GREEN)✓ Full CI pipeline complete$(NC)'

# ==============================================================================
# 📚 Documentation
# ==============================================================================

docs-setup:
	@python -c "from provide.foundry.config import extract_base_mkdocs; from pathlib import Path; extract_base_mkdocs(Path('.'))"

docs-build: docs-setup
	@mkdocs build

docs-serve: docs-setup
	@mkdocs serve

docs-clean:
	@rm -rf site .provide
