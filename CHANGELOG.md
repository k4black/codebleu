# Changelog

## Unreleased

- Automate release PRs and GitHub releases with Release Please and a GitHub App token.
- Replace Black, isort, and mypy with Ruff lint, Ruff format, and ty.

- Require Python 3.11 or later. Test Python 3.11 through 3.15 across Linux, Windows, and ARM and Intel macOS.
- Update Tree-sitter to 0.26.1 and all language grammars to current compatible releases.
- Update build, test, lint, Evaluate, and GitHub Actions dependencies. Remove unused test dependencies and obsolete stubs.
- Test installed wheels outside the checkout. Check valid syntax and metric components for all supported languages.
- Exclude local root files and obsolete parser binaries from source distributions.
- Build releases from their tags without changes to the protected branch or existing tags.
- Add Evaluate dependency updates and advisory Conventional Commit PR-title checks.

Grammar updates can change AST shapes and metric scores. The metric formulas remain unchanged.
