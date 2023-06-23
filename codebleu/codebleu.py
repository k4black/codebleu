# Copyright (c) Microsoft Corporation.
# Copyright (c) 2023 Konstantin Chernyshev.
# Licensed under the MIT license.
from pathlib import Path
from typing import Tuple, List, Dict, Optional, Callable

from . import bleu
from . import weighted_ngram_match
from . import syntax_match
from . import dataflow_match


PACKAGE_DIR = Path(__file__).parent
# AVAILABLE_LANGS = ['java', 'js', 'c_sharp', 'php', 'go', 'python', 'ruby']
AVAILABLE_LANGS = ['java', 'c_sharp', 'python']  # only keywords available


def calc_codebleu(
        predictions: List[str],
        references: List[str],
        lang: str,
        tokenizer: Optional[Callable] = None,
        weights: Tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25),
        keywords_dir: Path = PACKAGE_DIR / 'keywords',
        langso_so_file: Path = PACKAGE_DIR/ 'parser' / 'my-languages.so'
) -> Dict[str, float]:
    """Calculate CodeBLEU score

    Args:
        predictions: list of predictions
        references: list of lists with references
        lang: input language, one of AVAILABLE_LANGS
        tokenizer: tokenizer function, Defaults to lambda s: s.split()
        weights: weights of the ngram_match, weighted_ngram_match, syntax_match, and dataflow_match respectively

    Return:
        Scores dict
    """

    alpha, beta, gamma, theta = weights

    # preprocess inputs
    references = [[x.strip() for x in ref] if type(ref) == list else [ref.strip()] for ref in references]
    hypothesis = [x.strip() for x in predictions]

    if not len(references) == len(hypothesis):
        raise ValueError

    # calculate ngram match (BLEU)
    if tokenizer is None:
        tokenizer = lambda s: s.split()

    tokenized_hyps = [tokenizer(x) for x in hypothesis]
    tokenized_refs = [[tokenizer(x) for x in reference] for reference in references]

    ngram_match_score = bleu.corpus_bleu(tokenized_refs, tokenized_hyps)

    # calculate weighted ngram match
    keywords = [x.strip() for x in open(keywords_dir / (lang + '.txt'), 'r', encoding='utf-8').readlines()]

    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2
                for token in reference_tokens}
    tokenized_refs_with_weights = [[[reference_tokens, make_weights(reference_tokens, keywords)]
                                    for reference_tokens in reference] for reference in tokenized_refs]

    weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(
        tokenized_refs_with_weights, tokenized_hyps)

    # calculate syntax match
    syntax_match_score = syntax_match.corpus_syntax_match(
        references, hypothesis, lang, langso_so_file)

    # calculate dataflow match
    dataflow_match_score = dataflow_match.corpus_dataflow_match(
        references, hypothesis, lang, langso_so_file)

    print('ngram match: {0}, weighted ngram match: {1}, syntax_match: {2}, dataflow_match: {3}'.
          format(ngram_match_score, weighted_ngram_match_score, syntax_match_score, dataflow_match_score))

    code_bleu_score = alpha*ngram_match_score\
        + beta*weighted_ngram_match_score\
        + gamma*syntax_match_score\
        + theta*(dataflow_match_score or 1)

    print('CodeBLEU score: ', code_bleu_score)

    return {
        'codebleu': code_bleu_score,
        'ngram_match_score': ngram_match_score,
        'weighted_ngram_match_score': weighted_ngram_match_score,
        'syntax_match_score': syntax_match_score,
        'dataflow_match_score': dataflow_match_score
    }
