.PHONY: install update format isort black

install:
	uv sync --frozen --no-install-project --all-extras
	uv run pre-commit install
	npm install

update:
	uv lock --upgrade
	npm update

format:
	uv run ruff format && uv run ruff check --fix --select I
	npx prettier --write --plugin=prettier-plugin-solidity contracts/**/*.sol interfaces/**/*.sol

lint:
	uv run ruff check --fix

compile:
	brownie compile

test:
	pytest tests/ --pdb -vv
