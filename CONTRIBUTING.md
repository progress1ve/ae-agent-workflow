# Contributing

Open an issue with a minimal reproducible case, client/OS/AE/MCP versions, expected behavior and sanitized tool output. Install `requirements-dev.txt`, run `python -m unittest discover -s tests -v`, `python -m ruff check audio scripts tests`, and `python -m ruff format --check audio scripts tests`. Validate the skill frontmatter and local references. Document what was tested in native AE separately from helper-script tests.

Keep the skill concise. Add guidance after a reproducible failure, not after a hypothetical edge case. Preserve artist intent and existing authorization. Do not commit media, credentials, local configuration, logs or proprietary assets. Upstream AE bridge fixes belong upstream; link the issue here when useful.
