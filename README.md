# CodeBLEU
[![Publish](https://github.com/k4black/codebleu/actions/workflows/publish.yml/badge.svg)](https://github.com/k4black/codebleu/actions/workflows/publish.yml)
[![Test](https://github.com/k4black/codebleu/actions/workflows/test.yml/badge.svg)](https://github.com/k4black/codebleu/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/k4black/codebleu/branch/main/graph/badge.svg?token=60BIFPWRCE)](https://codecov.io/gh/k4black/codebleu)


Unofficial `CodeBLEU` implementation with pip and hf hub support.
Based on [CodeXGLUE/code-to-code-trans/evaluator/CodeBLEU](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans/evaluator/CodeBLEU) implementation.


---

## Description

> An ideal evaluation metric should consider the grammatical correctness and the logic correctness.
> We propose weighted n-gram match and syntactic AST match to measure grammatical correctness, and introduce semantic data-flow match to calculate logic correctness.
> ![CodeBLEU](CodeBLEU.jpg)
(from [CodeXGLUE](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans/evaluator/CodeBLEU))

In a nutshell, `CodeBLEU` is a weighted combination of `n-gram match (BLEU)`, `weighted n-gram match (BLEU-weighted)`, `AST match` and `data-flow match` scores.

The metric has shown higher correlation with human evaluation than `BLEU` and `accuracy` metrics.

--- 

This repository refactor the original implementation to make it more usable and comparable with pip and hf hub.


## Usage 

```python
from codebleu import calc_codebleu

pred = "def add ( a , b ) :\n return a + b"
ref = "def sum ( first , second ) :\n return second + first"

res = calc_codebleu([ref], [pred], "python")
print(res)
# {
#   'codebleu': 0.5537, 
#   'ngram_match_score': 0.1041, 
#   'weighted_ngram_match_score': 0.1109, 
#   'syntax_match_score': 1.0, 
#   'dataflow_match_score': 1.0
# }
```
where calc_codebleu takes the following arguments:
- `refarences`: `list[str]` or `list[list[str]]` of reference codes
- `predictions`: `list[str]` of predicted codes
- `lang`: `str` of language, see `codebleu.AVAILABLE_LANGS` for available languages (python, c_sharp, java at the moment)
- `weights`: weights of the `ngram_match`, `weighted_ngram_match`, `syntax_match`, and `dataflow_match` respectively
- `tokenizer`: `callable` to split code string to tokens, defaults to `s.split()`

and outputs the `dict[str, float]` with following fields:
- `codebleu`: the final `CodeBLEU` score
- `ngram_match_score`: `ngram_match` score (BLEU)
- `weighted_ngram_match_score`: `weighted_ngram_match` score (BLEU-weighted)
- `syntax_match_score`: `syntax_match` score (AST match)
- `dataflow_match_score`: `dataflow_match` score


## Installation

Requires Python 3.8+

The metrics can be installed with pip and used as indicated above:
```bash
pip install codebleu
```

TBA: 
alternatively the metric is available as [k4black/codebleu]() in `evaluate` (lib installation required):
```python
import evaluate
metric = evaluate.load("dvitel/codebleu")

pred = "def add ( a , b ) :\n return a + b"
ref = "def sum ( first , second ) :\n return second + first"

res = metric.compute([ref], [pred], "python")
print(res)
# {
#   'codebleu': 0.5537, 
#   'ngram_match_score': 0.1041, 
#   'weighted_ngram_match_score': 0.1109, 
#   'syntax_match_score': 1.0, 
#   'dataflow_match_score': 1.0
# }
```

## Citation

Official [CodeBLEU paper](https://arxiv.org/abs/2009.10297) can be cited as follows:
```bibtex
@misc{ren2020codebleu,
      title={CodeBLEU: a Method for Automatic Evaluation of Code Synthesis}, 
      author={Shuo Ren and Daya Guo and Shuai Lu and Long Zhou and Shujie Liu and Duyu Tang and Neel Sundaresan and Ming Zhou and Ambrosio Blanco and Shuai Ma},
      year={2020},
      eprint={2009.10297},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```