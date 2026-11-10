# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# Natural Language Toolkit: BLEU Score
#
# Copyright (C) 2001-2020 NLTK Project
# Authors: Chin Yee Lee, Hengfeng Li, Ruxin Hou, Calvin Tanujaya Lim
# Contributors: Björn Mattsson, Dmitrijs Milajevs, Liling Tan
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT


"""Weighted modified precision from CodeBLEU equations (2) and (3)."""

import math
from collections import Counter

from .bleu import SmoothingFunction, brevity_penalty, closest_ref_length
from .utils import ngrams


def sentence_bleu(references, hypothesis, weights=(1.0,), smoothing_function=None, auto_reweigh=False):
    """Score one hypothesis. Each reference is a [tokens, token_weights] pair."""
    return corpus_bleu([references], [hypothesis], weights, smoothing_function, auto_reweigh)


def corpus_bleu(list_of_references, hypotheses, weights=(1.0,), smoothing_function=None, auto_reweigh=False):
    """Calculate corpus precision with the paper's default weighted unigram order.

    Keyword weights apply to unigrams. Explicit higher orders use ordinary
    modified precision. Missing token weights default to 1.
    """
    assert len(list_of_references) == len(hypotheses), "The number of hypotheses and references must be the same"
    numerators, denominators = Counter(), Counter()
    hyp_lengths, ref_lengths = 0, 0
    for references, hypothesis in zip(list_of_references, hypotheses):
        if not references:
            raise ValueError("Each hypothesis must have at least one reference")
        for order in range(1, len(weights) + 1):
            numerator, denominator = modified_precision(references, hypothesis, order)
            numerators[order] += numerator
            denominators[order] += denominator
        hyp_lengths += len(hypothesis)
        ref_lengths += closest_ref_length([reference[0] for reference in references], len(hypothesis))
    if not numerators[1]:
        return 0.0
    if auto_reweigh and hyp_lengths < 4 and weights == (0.25, 0.25, 0.25, 0.25):
        weights = (1 / hyp_lengths,) * hyp_lengths
    precisions = [(numerators[order], denominators[order]) for order in range(1, len(weights) + 1)]
    if smoothing_function is None:
        smoothing_function = SmoothingFunction().method1
    precisions = smoothing_function(precisions, references=references, hypothesis=hypothesis, hyp_len=hyp_lengths)
    score = math.fsum(
        weight * math.log(numerator / denominator) for weight, (numerator, denominator) in zip(weights, precisions)
    )
    return brevity_penalty(ref_lengths, hyp_lengths) * math.exp(score)


def modified_precision(references, hypothesis, n):
    """Return weighted clipped candidate counts and weighted candidate counts."""
    counts = Counter(ngrams(hypothesis, n))
    max_counts = Counter()
    token_weights = {}
    for reference, reference_weights in references:
        max_counts |= Counter(ngrams(reference, n))
        for token, weight in reference_weights.items():
            token_weights[token] = max(token_weights.get(token, weight), weight)
    clipped = counts & max_counts
    if n == 1:
        numerator = sum(count * token_weights.get(ngram[0], 1) for ngram, count in clipped.items())
        denominator = sum(count * token_weights.get(ngram[0], 1) for ngram, count in counts.items())
    else:
        numerator = sum(clipped.values())
        denominator = sum(counts.values())
    return numerator, denominator or 1


# Keep the old import name for callers of the original evaluator.
modified_recall = modified_precision
