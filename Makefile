.DEFAULT_GOAL := help

.PHONY: help install-dev install-dev-codex install-dev-claude test

help:
	@printf '%s\n' \
	  'make install-dev         Install/update the dev skill for Codex and Claude Code' \
	  'make install-dev-codex   Install/update the dev skill for Codex only' \
	  'make install-dev-claude  Install/update the dev skill for Claude Code only' \
	  'make test               Run local tests without model calls'

install-dev:
	python3 scripts/install-dev-skill.py both

install-dev-codex:
	python3 scripts/install-dev-skill.py codex

install-dev-claude:
	python3 scripts/install-dev-skill.py claude

test:
	python3 -B -m unittest discover -s tests -v
