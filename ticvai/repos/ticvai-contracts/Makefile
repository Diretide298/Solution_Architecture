.PHONY: lint diff generate mock bundle

lint:
	npx @redocly/cli lint openapi/spine/*.yaml openapi/shared/*.yaml

diff:
	@./scripts/breaking-change-check.sh

bundle:
	@mkdir -p dist
	@for f in openapi/spine/*.yaml; do \
		npx @redocly/cli bundle $$f -o dist/$$(basename $$f); \
	done

generate: bundle
	@./scripts/generate-clients.sh

mock: bundle
	npx @stoplight/prism-cli mock dist/identity.yaml -p 4010 --dynamic
