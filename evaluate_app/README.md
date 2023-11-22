---
title: codebleu
tags:
- evaluate
- metric
- code
- codebleu
description: "Unofficial `CodeBLEU` implementation that supports Linux, MacOS and Windows."
sdk: gradio
sdk_version: 3.19.1
app_file: app.py
pinned: false
---

# Metric Card for codebleu

This repository contains an unofficial `CodeBLEU` implementation that supports `Linux`, `MacOS` and `Windows`. It is available through `PyPI` and the `evaluate` library.

Available for: `Python`, `C`, `C#`, `C++`, `Java`, `JavaScript`, `PHP`, `Go`, `Ruby`.

---

The code is based on the original [CodeXGLUE/CodeBLEU](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans/evaluator/CodeBLEU) and updated version by [XLCoST/CodeBLEU](https://github.com/reddy-lab-code-research/XLCoST/tree/main/code/translation/evaluator/CodeBLEU).  It has been refactored, tested, built for macOS and Windows, and multiple improvements have been made to enhance usability.

## Metric Description

> An ideal evaluation metric should consider the grammatical correctness and the logic correctness.
> We propose weighted n-gram match and syntactic AST match to measure grammatical correctness, and introduce semantic data-flow match to calculate logic correctness.
> ![CodeBLEU](CodeBLEU.jpg)  
[from [CodeXGLUE](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans/evaluator/CodeBLEU) repo]

In a nutshell, `CodeBLEU` is a weighted combination of `n-gram match (BLEU)`, `weighted n-gram match (BLEU-weighted)`, `AST match` and `data-flow match` scores.

The metric has shown higher correlation with human evaluation than `BLEU` and `accuracy` metrics.


## How to Use

### Inputs

- `refarences` (`list[str]` or `list[list[str]]`): reference code
- `predictions` (`list[str]`) predicted code
- `lang` (`str`): code language, see `codebleu.AVAILABLE_LANGS` for available languages (python, c_sharp c, cpp, javascript, java, php, go and ruby at the moment)
- `weights` (`tuple[float,float,float,float]`): weights of the `ngram_match`, `weighted_ngram_match`, `syntax_match`, and `dataflow_match` respectively, defaults to `(0.25, 0.25, 0.25, 0.25)`
- `tokenizer` (`callable`): to split code string to tokens, defaults to `s.split()`


### Output Values

[//]: # (*Explain what this metric outputs and provide an example of what the metric output looks like. Modules should return a dictionary with one or multiple key-value pairs, e.g. {"bleu" : 6.02}*)

[//]: # (*State the range of possible values that the metric's output can take, as well as what in that range is considered good. For example: "This metric can take on any value between 0 and 100, inclusive. Higher scores are better."*)

The metric outputs the `dict[str, float]` with following fields:
- `codebleu`: the final `CodeBLEU` score
- `ngram_match_score`: `ngram_match` score (BLEU)
- `weighted_ngram_match_score`: `weighted_ngram_match` score (BLEU-weighted)
- `syntax_match_score`: `syntax_match` score (AST match)
- `dataflow_match_score`: `dataflow_match` score

Each of the scores is in range `[0, 1]`, where `1` is the best score.


### Examples

[//]: # (*Give code examples of the metric being used. Try to include examples that clear up any potential ambiguity left from the metric description above. If possible, provide a range of examples that show both typical and atypical results, as well as examples where a variety of input parameters are passed.*)

Using pip package (`pip install codebleu`):
```python
from codebleu import calc_codebleu

prediction = "def add ( a , b ) :\n return a + b"
reference = "def sum ( first , second ) :\n return second + first"

result = calc_codebleu([reference], [prediction], lang="python", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
print(result)
{
  'codebleu': 0.5537, 
  'ngram_match_score': 0.1041, 
  'weighted_ngram_match_score': 0.1109, 
  'syntax_match_score': 1.0, 
  'dataflow_match_score': 1.0
}
```

Or using `evaluate` library (`codebleu` package required):
```python
import evaluate
metric = evaluate.load("k4black/codebleu")

prediction = "def add ( a , b ) :\n return a + b"
reference = "def sum ( first , second ) :\n return second + first"

result = metric.compute([reference], [prediction], lang="python", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
```

Note: `lang` is required;


## Limitations and Bias

[//]: # (*Note any known limitations or biases that the metric has, with links and references if possible.*)

This library requires `so` file compilation with tree-sitter, so it is platform dependent.  
Currently available for `Linux` (manylinux), `MacOS` and `Windows` with Python 3.8+.


## Citation
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

## Further References

The source code is available at GitHub [k4black/codebleu](https://github.com/k4black/codebleu) repository.
