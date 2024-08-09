.PHONY: install update format isort black

install:
	poetry install --no-root --sync
	npm install
	poetry run pre-commit install

update:
	poetry update
	npm update

format: isort black prettier

isort:
	isort .

black:
	black .

prettier:
	npx prettier --write --plugin=prettier-plugin-solidity contracts/**/*.sol interfaces/**/*.sol sandbox/**/*.sol
