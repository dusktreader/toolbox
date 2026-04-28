default: help


## ==== Site ============================================================================================================

site: site/serve  ## Shortcut for site/serve

site/build:  ## Build the static site
	@uv run zensical build --clean

site/serve:  ## Start a local dev server with live reload
	@uv run zensical serve --dev-addr localhost:12000


## ==== Data ============================================================================================================

refresh:  ## Fetch project data from PyPI and GitHub and update markdown
	@uv run toolbox


## ==== Quality Control =================================================================================================

qa: qa/lint qa/format-check  ## Run all quality checks

qa/lint:  ## Run linters
	@uv run ruff check src

qa/format:  ## Run code formatter
	@uv run ruff check --select I --fix src
	@uv run ruff format src

qa/format-check:  ## Check code formatting without modifying files
	@uv run ruff format --check src


## ==== Helpers =========================================================================================================

clean:  ## Clean up build artifacts
	@rm -rf site
	@rm -rf .ruff_cache
	@uv run pyclean . --debris 2>/dev/null || true

help:  ## Show help message
	@awk "$$PRINT_HELP_PREAMBLE" $(MAKEFILE_LIST)


# ..... Make configuration .............................................................................................

.ONESHELL:
SHELL:=/bin/bash
.PHONY: site site/build site/serve \
	refresh \
	qa qa/lint qa/format qa/format-check \
	clean help


# ..... Color table for pretty printing ................................................................................

RED    := \033[31m
GREEN  := \033[32m
YELLOW := \033[33m
BLUE   := \033[34m
TEAL   := \033[36m
GRAY   := \033[90m
CLEAR  := \033[0m
ITALIC := \033[3m


# ..... Help printer ...................................................................................................

define PRINT_HELP_PREAMBLE
BEGIN {
	print "Usage: $(YELLOW)make <target>$(CLEAR)"
	print
	print "Targets:"
}
/^## =+ .+( =+)?/ {
    s = $$0
    sub(/^## =+ /, "", s)
    sub(/ =+/, "", s)
	printf("\n  %s:\n", s)
}
/^## -+ .+( -+)?/ {
    s = $$0
    sub(/^## -+ /, "", s)
    sub(/ -+/, "", s)
	printf("\n    $(TEAL)> %s$(CLEAR)\n", s)
}
/^[$$()% 0-9a-zA-Z_\/-]+(\\:[$$()% 0-9a-zA-Z_\/-]+)*:.*?##/ {
    t = $$0
    sub(/:.*/, "", t)
    h = $$0
    sub(/.?*##/, "", h)
    printf("    $(YELLOW)%-19s$(CLEAR) $(GRAY)$(ITALIC)%s$(CLEAR)\n", t, h)
}
endef
export PRINT_HELP_PREAMBLE
