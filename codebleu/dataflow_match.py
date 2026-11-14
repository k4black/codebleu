# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
import logging

from tree_sitter import Parser

from .parser import (
    DFG_csharp,
    DFG_fortran,
    DFG_go,
    DFG_java,
    DFG_javascript,
    DFG_php,
    DFG_python,
    DFG_ruby,
    DFG_rust,
    index_to_code_token,
    remove_comments_and_docstrings,
    tree_to_token_index,
)
from .utils import get_tree_sitter_language

dfg_function = {
    "python": DFG_python,
    "java": DFG_java,
    "ruby": DFG_ruby,
    "go": DFG_go,
    "php": DFG_php,
    "javascript": DFG_javascript,
    "typescript": DFG_javascript,
    "tsx": DFG_javascript,
    "fortran": DFG_fortran,
    "c_sharp": DFG_csharp,
    "c": DFG_csharp,  # XLCoST uses C# parser for C
    "cpp": DFG_csharp,  # XLCoST uses C# parser for C++
    "rust": DFG_rust,
}


def calc_dataflow_match(references, candidate, lang, langso_so_file):
    return corpus_dataflow_match([references], [candidate], lang, langso_so_file)


def corpus_dataflow_match(references, candidates, lang, tree_sitter_language=None):
    if not tree_sitter_language:
        tree_sitter_language = get_tree_sitter_language(lang)

    parser = Parser()
    parser.language = tree_sitter_language
    parser = [parser, dfg_function[lang]]
    match_count = 0
    total_count = 0

    for i in range(len(candidates)):
        references_sample = references[i]
        candidate = candidates[i]
        for reference in references_sample:
            try:
                candidate = remove_comments_and_docstrings(candidate, lang)
            except Exception:
                pass
            try:
                reference = remove_comments_and_docstrings(reference, lang)
            except Exception:
                pass

            cand_dfg = get_data_flow(candidate, parser)
            ref_dfg = get_data_flow(reference, parser)

            normalized_cand_dfg = normalize_dataflow(cand_dfg)
            normalized_ref_dfg = normalize_dataflow(ref_dfg)

            if len(normalized_ref_dfg) > 0:
                total_count += len(normalized_ref_dfg)
                for dataflow in normalized_ref_dfg:
                    if dataflow in normalized_cand_dfg:
                        match_count += 1
                        normalized_cand_dfg.remove(dataflow)
    if total_count == 0:
        logging.warning(
            "WARNING: There is no reference data-flows extracted from the whole corpus, "
            "and the data-flow match score degenerates to 0. Please consider ignoring this score."
        )
        return 0
    score = match_count / total_count
    return score


def get_data_flow(code, parser):
    try:
        tree = parser[0].parse(bytes(code, "utf8"))
        root_node = tree.root_node
        tokens_index = tree_to_token_index(root_node)
        code = code.split("\n")
        code_tokens = [index_to_code_token(x, code) for x in tokens_index]
        index_to_code = {}
        for idx, (index, code) in enumerate(zip(tokens_index, code_tokens)):
            index_to_code[index] = (idx, code)
        try:
            DFG, _ = parser[1](root_node, index_to_code, {})
        except Exception:
            DFG = []
        DFG = sorted(DFG, key=lambda x: x[1])
        indexs = set()
        for d in DFG:
            if len(d[-1]) != 0:
                indexs.add(d[1])
            for x in d[-1]:
                indexs.add(x)
        new_DFG = []
        for d in DFG:
            if d[1] in indexs:
                new_DFG.append(d)
        dfg = new_DFG
    except Exception:
        code.split()
        dfg = []
    # Rebuild paired dependencies from token positions, including repeated names.
    names_by_position = {item[1]: item[0] for item in dfg}
    merged = {}
    for name, position, relationship, _, parents in dfg:
        previous = merged.get(position)
        positions = sorted(set(parents + (previous[4] if previous else [])))
        names = [names_by_position.get(parent, code_tokens[parent]) for parent in positions]
        merged[position] = (name, position, relationship, names, positions)
    return [merged[position] for position in sorted(merged)]


def normalize_dataflow_item(dataflow_item):
    return normalize_dataflow([dataflow_item])[0]


def normalize_dataflow(dataflow):
    var_dict = {}
    i = 0
    normalized_dataflow = []
    for item in dataflow:
        var_name = item[0]
        relationship = item[2]
        par_vars_name_list = item[3]
        for name in par_vars_name_list:
            if name not in var_dict:
                var_dict[name] = "var_" + str(i)
                i += 1
        if var_name not in var_dict:
            var_dict[var_name] = "var_" + str(i)
            i += 1
        normalized_dataflow.append(
            (
                var_dict[var_name],
                relationship,
                [var_dict[x] for x in par_vars_name_list],
            )
        )
    return normalized_dataflow
