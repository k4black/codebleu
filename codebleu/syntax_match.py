# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from collections import Counter

from tree_sitter import Parser

from .parser import remove_comments_and_docstrings
from .utils import get_tree_sitter_language


def calc_syntax_match(references, candidate, lang):
    return corpus_syntax_match([references], [candidate], lang)


def corpus_syntax_match(references, candidates, lang, tree_sitter_language=None):
    if tree_sitter_language is None:
        tree_sitter_language = get_tree_sitter_language(lang)
    parser = Parser(tree_sitter_language)
    match_count = 0
    total_count = 0

    def subtrees(code):
        try:
            code = remove_comments_and_docstrings(code, lang)
        except Exception:
            pass
        stack = [parser.parse(code.encode("utf-8")).root_node]
        counts = Counter()
        while stack:
            node = stack.pop()
            if node.children:
                counts[str(node)] += 1
                stack.extend(node.children)
        return counts

    for references_sample, candidate in zip(references, candidates):
        candidate_counts = subtrees(candidate)
        for reference in references_sample:
            reference_counts = subtrees(reference)
            match_count += sum((candidate_counts & reference_counts).values())
            total_count += sum(reference_counts.values())
    return match_count / total_count if total_count else 0.0
