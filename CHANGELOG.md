# Changelog

## Unreleased

- Change scores to follow the paper's weighted unigram precision, reference lengths, and clipped AST counts.
- Preserve zero data-flow credit and deterministic dependency normalization. Remove duplicated BLEU helpers.
- Reject empty reference sets and document discrepancies between the paper and its official evaluator.

- Require Python 3.11 or later. Test Python 3.11 through 3.15 across Linux, Windows, and ARM and Intel macOS.
- Update Tree-sitter to 0.26.1 and all language grammars to current compatible releases.
- Update build, test, lint, Evaluate, and GitHub Actions dependencies. Remove unused test dependencies and obsolete stubs.
- Test installed wheels outside the checkout. Check valid syntax and metric components for all supported languages.
- Exclude local root files and obsolete parser binaries from source distributions.
- Build releases from their tags without changes to the protected branch or existing tags.
- Add Evaluate dependency updates and advisory Conventional Commit PR-title checks.

Grammar updates and the metric corrections above change scores. See `docs/metric-semantics.md` before comparing releases.
