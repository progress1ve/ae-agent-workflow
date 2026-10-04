# Contributing

Open an issue with a minimal reproducible case, client/OS/AE/MCP versions, expected behavior and sanitized tool output. For changes, run `python -m unittest discover -s tests -v` and skill validation. Document what was tested in native AE separately from helper-script tests.

Keep the skill concise. Add guidance after a reproducible failure, not after a hypothetical edge case. Preserve artist intent and existing authorization. Do not commit media, credentials, local configuration, logs or proprietary assets. Upstream AE bridge fixes belong upstream; link the issue here when useful.
