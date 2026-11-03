.PHONY: lint diff generate mock bundle

# openapi/ is a copy of every folder of the package's contracts/, refreshed by tools/derive-mirrors.py. shared/ holds
# components only, so it is linted and never bundled (r13 system review D-10, CHG-R14J-003: devices/ was left out).
lint:
	npx @redocly/cli lint openapi/*/*.yaml

diff:
	@./scripts/breaking-change-check.sh

bundle:
	@mkdir -p dist
	@for f in $$(ls openapi/*/*.yaml | grep -v '^openapi/shared/'); do \
		npx @redocly/cli bundle $$f -o dist/$$(basename $$(dirname $$f))-$$(basename $$f); \
	done

generate: bundle
	@./scripts/generate-clients.sh

mock: bundle
	npx @stoplight/prism-cli mock dist/spine-identity.yaml -p 4010 --dynamic
