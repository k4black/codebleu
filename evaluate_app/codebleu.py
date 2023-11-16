# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TODO: Add a description here."""
import importlib

import datasets
import evaluate

_CITATION = """\
@misc{ren2020codebleu,
      title={CodeBLEU: a Method for Automatic Evaluation of Code Synthesis}, 
      author={Shuo Ren and Daya Guo and Shuai Lu and Long Zhou and Shujie Liu and Duyu Tang and Neel Sundaresan and Ming Zhou and Ambrosio Blanco and Shuai Ma},
      year={2020},
      eprint={2009.10297},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
"""

_DESCRIPTION = """\
Unofficial `CodeBLEU` implementation that supports Linux and MacOS.
"""


_KWARGS_DESCRIPTION = """
Calculate a weighted combination of `n-gram match (BLEU)`, `weighted n-gram match (BLEU-weighted)`, `AST match` and `data-flow match` scores.

Args:
    predictions: list of predictions to score. Each predictions
        should be a string with tokens separated by spaces.
    references: list of reference for each prediction. Each
        reference should be a string with tokens separated by spaces.
    language: programming language in ['java','js','c_sharp','php','c','python','cpp'].
    weights: tuple of 4 floats to use as weights for scores. Defaults to (0.25, 0.25, 0.25, 0.25).
Returns:
    codebleu: resulting `CodeBLEU` score,
    ngram_match_score: resulting `n-gram match (BLEU)` score,
    weighted_ngram_match_score: resulting `weighted n-gram match (BLEU-weighted)` score,
    syntax_match_score: resulting `AST match` score,
    dataflow_match_score: resulting `data-flow match` score,
Examples:
    >>> metric = evaluate.load("k4black/codebleu")
    >>> ref = "def sum ( first , second ) :\n return second + first"
    >>> pred = "def add ( a , b ) :\n return a + b"
    >>> results = metric.compute(references=[ref], predictions=[pred], language="python")
    >>> print(results)
"""


@evaluate.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class codebleu(evaluate.Metric):
    """CodeBLEU metric from CodexGLUE"""

    def _info(self):
        # TODO: Specifies the evaluate.EvaluationModuleInfo object
        return evaluate.MetricInfo(
            # This is the description that will appear on the modules page.
            module_type="metric",
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            # This defines the format of each prediction and reference
            features=[
                datasets.Features(
                    {
                        "predictions": datasets.Value("string", id="sequence"),
                        "references": datasets.Sequence(datasets.Value("string", id="sequence"), id="references"),
                        "lang": datasets.Value("string"),
                        # "weights": datasets.Value("string"),
                        # "tokenizer": datasets.Value("string"),
                    }
                ),
                datasets.Features(
                    {
                        "predictions": datasets.Value("string", id="sequence"),
                        "references": datasets.Value("string", id="sequence"),
                        "lang": datasets.Value("string"),
                        # "weights": datasets.Value("string"),
                        # "tokenizer": datasets.Value("string"),
                    }
                ),
            ],
            # Homepage of the module for documentation
            homepage="https://github.com/k4black/codebleu",
            # Additional links to the codebase or references
            codebase_urls=["https://github.com/k4black/codebleu"],
            reference_urls=[
                "https://github.com/k4black/codebleu",
                "https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans/evaluator",
                "https://arxiv.org/abs/2009.10297",
            ],
        )

    def _download_and_prepare(self, dl_manager):
        """Optional: download external resources useful to compute the scores"""
        # workarounds as this file have to be named codebleu (evaluate library requirement)
        self.codebleu_package = importlib.import_module("codebleu")
        pass

    def _compute(self, predictions, references, lang, weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None):
        """Returns the scores"""
        return self.codebleu_package.calc_codebleu(
            references=references,
            predictions=predictions,
            lang=lang,
            weights=weights,
            tokenizer=tokenizer,
        )
