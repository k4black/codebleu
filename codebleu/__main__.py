# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# -*- coding:utf-8 -*-
import argparse
from pathlib import Path
from typing import List, Tuple

from . import calc_codebleu

PACKAGE_DIR = Path(__file__).parent


def main(
    ref_files: List[str],
    hyp_file: str,
    lang: str,
    weights: Tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25),
) -> None:
    pre_references = [[x.strip() for x in open(file, "r", encoding="utf-8").readlines()] for file in ref_files]
    hypothesis = [x.strip() for x in open(hyp_file, "r", encoding="utf-8").readlines()]

    for i in range(len(pre_references)):
        assert len(hypothesis) == len(pre_references[i])

    references = []
    for i in range(len(hypothesis)):
        ref_for_instance = []
        for j in range(len(pre_references)):
            ref_for_instance.append(pre_references[j][i])
        references.append(ref_for_instance)
    assert len(references) == len(pre_references) * len(hypothesis)

    code_bleu_score = calc_codebleu(
        references,
        hypothesis,
        lang,
        weights=weights,
    )

    print(
        f"ngram_match: {code_bleu_score['ngram_match_score']}",
        f"weighted_ngram_match: {code_bleu_score['weighted_ngram_match_score']}",
        f"syntax_match: {code_bleu_score['syntax_match_score']}",
        f"dataflow_match: {code_bleu_score['dataflow_match_score']}",
    )

    print("CodeBLEU score: ", code_bleu_score["codebleu"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--refs", type=str, nargs="+", required=True, help="reference files")
    parser.add_argument("--hyp", type=str, required=True, help="hypothesis file")
    parser.add_argument(
        "--lang",
        type=str,
        required=True,
        choices=["java", "js", "c_sharp", "php", "go", "python", "ruby"],
    )
    parser.add_argument("--params", type=str, default="0.25,0.25,0.25,0.25", help="alpha, beta and gamma")

    args = parser.parse_args()

    lang = args.lang
    alpha, beta, gamma, theta = [float(x) for x in args.params.split(",")]

    main(
        args.refs,
        args.hyp,
        args.lang,
        weights=(alpha, beta, gamma, theta),
    )
