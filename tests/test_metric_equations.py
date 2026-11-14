import json
import os
import subprocess
import sys

import pytest
from tree_sitter import Parser

from codebleu import bleu, calc_codebleu, weighted_ngram_match
from codebleu.dataflow_match import dfg_function, get_data_flow, normalize_dataflow_item
from codebleu.syntax_match import corpus_syntax_match
from codebleu.utils import get_tree_sitter_language


@pytest.mark.parametrize(
    ("references", "hypothesis", "expected"),
    [
        ([(["a"], {"a": 0.2})], ["a"], 1.0),
        ([(["a", "b"], {"a": 1, "b": 1})], ["a", "b", "b"], 2 / 3),
        ([(["a", "b", "c", "d"], {})], ["a", "b"], 0.36787944117144233),
        ([(["a", "b"], {}), (["a", "c"], {})], ["a", "b"], 1.0),
        ([(["a", "a"], {}), (["a", "a"], {})], ["a", "a", "a"], 2 / 3),
        ([(["a"], {})], ["b"], 0.0),
        ([(["a"], {})], [], 0.0),
    ],
)
def test_weighted_unigram_equation(references, hypothesis, expected):
    assert weighted_ngram_match.corpus_bleu([references], [hypothesis]) == pytest.approx(expected)


@pytest.mark.parametrize("weights", [(1.0,), (0.25, 0.25, 0.25, 0.25)])
def test_equal_token_weights_match_bleu_at_the_same_order(weights):
    references = [["a b c d e f".split(), "a b c d x y".split()]]
    hypothesis = ["a b c d z".split()]
    weighted = [[[reference, dict.fromkeys(reference + hypothesis[0], 1)] for reference in references[0]]]
    assert weighted_ngram_match.corpus_bleu(weighted, hypothesis, weights) == pytest.approx(
        bleu.corpus_bleu(references, hypothesis, weights)
    )


def test_candidate_keywords_receive_keyword_weights():
    result = calc_codebleu(["alpha beta"], ["alpha return"], "python")
    # One matching non-keyword (0.2), divided by a non-keyword plus a keyword (1.2).
    assert result["weighted_ngram_match_score"] == pytest.approx(1 / 6)


@pytest.mark.parametrize("weights", [(0.25, 0.25, 0.25, 0.25), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 0.0)])
def test_zero_dataflow_does_not_receive_full_credit(weights):
    result = calc_codebleu(["a = 1\nb = a"], ["pass"], "python", weights=weights)
    assert result["dataflow_match_score"] == 0.0
    assert result["codebleu"] == 0.0


@pytest.mark.parametrize(
    ("reference", "candidate", "expected"),
    [("x = 1\nx = 1", "x = 1", 2 / 5), ("x = 1", "x = 1\nx = 1", 2 / 3), ("", "", 0.0)],
)
def test_ast_matches_clip_duplicate_subtrees(reference, candidate, expected):
    assert corpus_syntax_match([[reference]], [candidate], "python") == pytest.approx(expected)


def test_dataflow_dependencies_keep_names_and_positions_paired():
    parser = Parser(get_tree_sitter_language("python"))
    dataflow = get_data_flow("a = 1\nb = 2\nc = a + b", [parser, dfg_function["python"]])
    assert ("c", 6, "computedFrom", ["a", "b"], [8, 10]) in dataflow


def test_single_dataflow_item_uses_first_appearance_normalization():
    assert normalize_dataflow_item(("z", 2, "computedFrom", ["x", "y"], [0, 1])) == (
        "var_2",
        "computedFrom",
        ["var_0", "var_1"],
    )


def test_dataflow_is_identical_across_hash_seeds():
    script = """
import json
from tree_sitter import Parser
from codebleu.dataflow_match import dfg_function, get_data_flow, normalize_dataflow
from codebleu.utils import get_tree_sitter_language
code = "a = 1\\nb = 2\\nc = a + b\\nfor i in range(2):\\n    c = a + b\\nresult = c"
parser = Parser(get_tree_sitter_language("python"))
print(json.dumps(normalize_dataflow(get_data_flow(code, [parser, dfg_function["python"]]))))
"""
    results = [
        subprocess.run(
            [sys.executable, "-c", script],
            env={**os.environ, "PYTHONHASHSEED": seed},
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        for seed in ("1", "7", "42")
    ]
    assert json.loads(results[0])
    assert results[0] == results[1] == results[2]


@pytest.mark.parametrize(("references", "predictions"), [([], []), ([[]], ["pass"])])
def test_empty_reference_sets_have_a_clear_error(references, predictions):
    with pytest.raises(ValueError, match="references must contain"):
        calc_codebleu(references, predictions, "python")


def test_empty_programs_have_zero_components():
    assert calc_codebleu([""], [""], "python") == {
        "codebleu": 0.0,
        "ngram_match_score": 0.0,
        "weighted_ngram_match_score": 0.0,
        "syntax_match_score": 0.0,
        "dataflow_match_score": 0.0,
    }


@pytest.mark.parametrize(
    "reference",
    [
        "def f(x, y):\n    if x:\n        z = x\n    else:\n        z = y\n    return z",
        "def f(x, y):\n    z = x\n    while z < y:\n        z = z + x\n    return z",
        "def f(x, y):\n    z = x\n    for i in range(y):\n        z = z + x\n    return z",
    ],
)
def test_control_flow_matches_after_variable_renaming(reference):
    candidate = reference.replace("x", "first").replace("y", "second").replace("z", "result")
    result = calc_codebleu([reference], [candidate], "python")
    assert result["dataflow_match_score"] == 1.0
    assert result["syntax_match_score"] == 1.0


@pytest.mark.parametrize(("auto_reweigh", "expected"), [(False, 0.31622776601683794), (True, 1.0)])
def test_explicit_four_gram_sentence_scores_keep_short_sentence_reweighting(auto_reweigh, expected):
    score = weighted_ngram_match.sentence_bleu(
        [(["a", "b"], {})], ["a", "b"], weights=(0.25, 0.25, 0.25, 0.25), auto_reweigh=auto_reweigh
    )
    assert score == pytest.approx(expected)


def test_weighted_component_rejects_missing_references():
    with pytest.raises(ValueError, match="at least one reference"):
        weighted_ngram_match.corpus_bleu([[]], [["a"]])


def test_incomplete_python_programs_remain_scoreable():
    result = calc_codebleu(["def f("], ["def f("], "python")
    assert result["syntax_match_score"] == 1.0
    assert result["weighted_ngram_match_score"] == 1.0
    assert result["dataflow_match_score"] == 0.0
