# Metric definitions and score changes

This implementation follows the explicit equations in [CodeBLEU, sections 3.1–3.3](https://arxiv.org/html/2009.10297).
It is not numerically compatible with every published example or earlier package release.
Record the package, Tree-sitter, and grammar versions with evaluation results.

## Reference implementation

The comparison used Microsoft's official evaluator at commit [`50a483084fd5641889e1afb1c4c253f3987b5660`](https://github.com/microsoft/CodeXGLUE/tree/50a483084fd5641889e1afb1c4c253f3987b5660/Code-Code/code-to-code-trans/evaluator/CodeBLEU).
That commit is fixed so that the comparison remains reproducible.
The official evaluator contains some of the defects reported against this package.
Matching that code alone does not establish agreement with the paper.

| Component | Official evaluator or previous package | Corrected behavior |
|---|---|---|
| Final score | This package replaces a zero data-flow score with one. The official evaluator does not. | Use the four reported components directly in equation (1). |
| Weighted precision | `modified_recall` divides by reference counts and sums scores over separate references. | Divide weighted clipped candidate counts by weighted candidate counts, with maximum reference counts. |
| Brevity penalty | The weighted evaluator measures the `[tokens, weights]` wrapper as length two. | Use actual reference token lengths. |
| Weighted order | The official evaluator defaults to four orders. | Default to weighted unigrams. Explicit higher orders remain available through the component API. |
| AST matching | Membership checks can reuse one candidate subtree for multiple reference occurrences. | Clip subtree occurrence counts before division by the reference count. |
| Data-flow merging | Independent sets lose dependency order and the association between names and positions. | Rebuild paired dependencies in token-position order before normalization. |

Relevant official files:

- [Final combination](https://github.com/microsoft/CodeXGLUE/blob/50a483084fd5641889e1afb1c4c253f3987b5660/Code-Code/code-to-code-trans/evaluator/CodeBLEU/calc_code_bleu.py)
- [Weighted match](https://github.com/microsoft/CodeXGLUE/blob/50a483084fd5641889e1afb1c4c253f3987b5660/Code-Code/code-to-code-trans/evaluator/CodeBLEU/weighted_ngram_match.py)
- [AST match](https://github.com/microsoft/CodeXGLUE/blob/50a483084fd5641889e1afb1c4c253f3987b5660/Code-Code/code-to-code-trans/evaluator/CodeBLEU/syntax_match.py)
- [Data-flow match](https://github.com/microsoft/CodeXGLUE/blob/50a483084fd5641889e1afb1c4c253f3987b5660/Code-Code/code-to-code-trans/evaluator/CodeBLEU/dataflow_match.py)

The lexical comparison ran the pinned weighted evaluator with its n-gram helper import redirected to this package's equivalent helper.
The original parser API does not load with current Tree-sitter bindings.
The AST comparison therefore uses source inspection and tests against the declared modern grammars.
It does not claim to reproduce the original parser binaries.

## Decisions where sources disagree

Section 3.1 specifies `N = 1` and `w_n = 1` for weighted matching.
The released code uses four orders, with keyword weights only on unigrams.
The published weighted examples reproduce that four-order code, rather than the stated unigram definition.
This package now follows the explicit unigram definition.
It retains the stated keyword ratio of 5:1, which the official code represents as `1` and `0.2`.
The phrase about four times more weight in Example 1 does not establish a separate ratio correction.

Candidate tokens receive their keyword weights even if no reference contains them.
The denominator includes all candidate tokens.
A short exact match with fractional weights can score one. Its denominator is not clamped to one.
With equal token weights, compare weighted matching with ordinary BLEU at the same n-gram order.
The default weighted unigram score is not expected to equal default four-gram BLEU.

## Published examples

The following scores use the Java grammar declared in `pyproject.toml`.
Rows correspond to the existing test cases from the official example and paper examples 1 and 2.

| Example | BLEU | Corrected weighted unigram | Clipped AST | Data flow | Final score |
|---|---:|---:|---:|---:|---:|
| Complete example with type and variable changes | 0.784626 | 51/58 | 8/19 | 2/3 | 0.687914 |
| Paper example 1, missing closing brace | 0.754251 | 0.851010 | 8/19 | 2/3 | 0.673245 |
| Paper example 2, renamed variable | 0.757139 | 55/58 | 1 | 1 | 0.926354 |

For the missing-brace example, weighted precision is `50/57` and the brevity penalty is `exp(1 - 34/33)`.
The pinned official weighted evaluator returns `0.777549`, `0.749138`, and `0.764608` for these three examples.
Those values differ from weighted unigram precision.
The paper's AST example uses 21 reference subtrees. The current Java grammar produces 19.
Clipping repeated subtree occurrences also changes the numerator.
The paper's Figure 4 label disagrees with its accompanying BLEU text. The calculated BLEU agrees with the text.

## Empty and multiple-reference cases

The public API rejects an empty corpus or a sample without a reference.
Empty program strings remain valid inputs and produce zero components when both programs are empty.
A corpus without reference data flows keeps the official warning and zero data-flow score.
The final score gives that component zero credit. It does not change the component weights.
Thus an exact match without reference data flows can score less than one.

Weighted precision clips against the maximum counts across references.
AST and data-flow matching retain the official aggregation across reference pairs.
This change does not introduce a new best-reference policy for those components.

## Limits

CodeBLEU measures token, structure, and dependency similarity.
It does not execute programs or prove semantic equivalence.
Identical scores for programs with different behavior do not alone establish an implementation defect, as discussed in issue #32.
Use execution tests when behavioral correctness matters.
Language extraction remains approximate.
