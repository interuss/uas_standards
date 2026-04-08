.PHONY: apis
apis:
	./tools/openapi_conversion/generate_apis.sh

.PHONY: test
test:
	PYTHONPATH="$(PYTHONPATH):./src" uv run pytest tests/

.PHONY: lint
lint:
	uv run --index https://pypi.org/simple ruff format --check
	uv run --index https://pypi.org/simple ruff check
	uv run --index https://pypi.org/simple --all-groups basedpyright
