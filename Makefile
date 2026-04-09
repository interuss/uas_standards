.PHONY: apis
apis:
	./tools/openapi_conversion/generate_apis.sh

.PHONY: test
test:
	PYTHONPATH="$(PYTHONPATH):./src" uv run pytest tests/

.PHONY: lint
lint:
	uv run ruff format --check
	uv run ruff check
	uv run --all-groups basedpyright
