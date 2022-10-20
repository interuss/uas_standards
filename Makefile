.PHONY: apis
apis:
	./tools/openapi_conversion/generate_apis.sh

.PHONY: test
test:
	PYTHONPATH="$(PYTHONPATH):./src" pytest tests/