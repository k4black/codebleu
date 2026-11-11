import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest
from tree_sitter import Parser

from codebleu.dataflow_match import dfg_function, get_data_flow
from codebleu.parser import DFG_fortran, index_to_code_token, remove_comments_and_docstrings, tree_to_token_index
from codebleu.utils import get_tree_sitter_language


@pytest.mark.parametrize(
    ("lang", "code", "name", "relationship", "parents"),
    [
        ("rust", "fn foo(x: i32) -> i32 { let y = x; y }", "y", "comesFrom", ["x"]),
        ("rust", "fn foo(x: i32) -> i32 { let mut y = 0; y = x; y }", "y", "computedFrom", ["x"]),
        ("rust", "fn foo(x: i32) { for i in 0..x { let y = i; } }", "i", "computedFrom", ["0", "x"]),
        ("typescript", "let x: number = 1; let y: number = x;", "y", "comesFrom", ["x"]),
        ("rust", "fn foo(x: i32) -> i32 { let mut y = 0; y += x; y }", "y", "computedFrom", ["x", "y"]),
        ("typescript", "let x = 1; let y = 0; y += x;", "y", "computedFrom", ["x", "y"]),
        ("typescript", "let x = 1; let y = 0; y = x;", "y", "computedFrom", ["x"]),
        ("tsx", "const x = 1; const y = <span>{x}</span>;", "y", "comesFrom", ["x"]),
        ("fortran", "program main\ninteger :: x = 1, y\ny = x\nend program", "y", "computedFrom", ["x"]),
        ("fortran", "program main\ninteger :: X = 1, Y\nY = x\nend program", "y", "computedFrom", ["x"]),
        (
            "fortran",
            "program main\ninteger :: x = 2, i\ndo i = 1, x\nprint *, i\nend do\nend program",
            "i",
            "computedFrom",
            ["1", "x"],
        ),
    ],
)
def test_language_dependencies(lang: str, code: str, name: str, relationship: str, parents: list[str]) -> None:
    parser = Parser(get_tree_sitter_language(lang))
    assert not parser.parse(code.encode("utf-8")).root_node.has_error
    dataflow = get_data_flow(code, [parser, dfg_function[lang]])
    assert any(item[0] == name and item[2] == relationship and sorted(item[3]) == parents for item in dataflow)


def test_fortran_comments_preserve_strings_and_concatenation() -> None:
    source = "value = 'a!b' // 'c' ! remove this comment"
    assert remove_comments_and_docstrings(source, "fortran") == "value = 'a!b' // 'c'  "


def test_console_help() -> None:
    command = Path(sysconfig.get_path("scripts")) / ("codebleu.exe" if sys.platform == "win32" else "codebleu")
    result = subprocess.run([str(command), "--help"], capture_output=True, text=True, check=True)
    assert "typescript" in result.stdout
    assert "fortran" in result.stdout


def test_module_accepts_multiple_references(tmp_path: Path) -> None:
    code = "function foo ( x : number ) : number { return x ; }\n"
    reference = tmp_path / "reference.txt"
    hypothesis = tmp_path / "hypothesis.txt"
    reference.write_text(code, encoding="utf-8")
    hypothesis.write_text(code, encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "codebleu",
            "--refs",
            str(reference),
            str(reference),
            "--hyp",
            str(hypothesis),
            "--lang",
            "typescript",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "CodeBLEU score:  1.0" in result.stdout


def test_fortran_keeps_both_branch_definitions() -> None:
    code = "program main\ninteger :: x = 1, y\nif (x > 0) then\ny = x\nelse\ny = 2\nend if\nend program"
    root = Parser(get_tree_sitter_language("fortran")).parse(code.encode("utf-8")).root_node
    assert not root.has_error
    index_to_code = {
        index: (position, index_to_code_token(index, code.split("\n")))
        for position, index in enumerate(tree_to_token_index(root))
    }
    _, states = DFG_fortran(root, index_to_code, {})
    assert len(states["y"]) == 2


@pytest.mark.parametrize(
    ("body", "definitions"),
    [
        ("if x > 0 { y = x; } else { y = 1; }", [21, 28]),
        ("if x > 0 { y = x; }", [12, 21]),
        ("if x > 0 { y = x; } else if x < 0 { y = 2; } else { y = 1; }", [21, 32, 39]),
    ],
)
def test_rust_branch_reads_reach_each_definition(body: str, definitions: list[int]) -> None:
    code = f"fn f(x: i32) -> i32 {{ let mut y = 0; {body} y }}"
    parser = Parser(get_tree_sitter_language("rust"))
    assert not parser.parse(code.encode("utf-8")).root_node.has_error
    dataflow = get_data_flow(code, [parser, dfg_function["rust"]])
    assert dataflow[-1][0] == "y"
    assert dataflow[-1][4] == definitions


@pytest.mark.parametrize("target", ["a(i)", "a(i + 1)", "a(i:i+1)"])
def test_fortran_array_assignment_preserves_index_definition(target: str) -> None:
    code = f"program main\ninteger :: a(3), i = 1, x = 2\n{target} = x\nprint *, i\nend program"
    parser = Parser(get_tree_sitter_language("fortran"))
    assert not parser.parse(code.encode("utf-8")).root_node.has_error
    dataflow = get_data_flow(code, [parser, dfg_function["fortran"]])
    assert not any(item[0] == "i" and item[2] == "computedFrom" and "x" in item[3] for item in dataflow)
    assert dataflow[-1][0] == "i"
    assert dataflow[-1][4] == [9]


@pytest.mark.parametrize("element", ["<components.Button />", "<components.Button></components.Button>"])
def test_tsx_qualified_component_keeps_dependency(element: str) -> None:
    code = f"const components = {{ Button: () => null }}; const node = {element};"
    parser = Parser(get_tree_sitter_language("tsx"))
    assert not parser.parse(code.encode("utf-8")).root_node.has_error
    dataflow = get_data_flow(code, [parser, dfg_function["tsx"]])
    assert any(item[0] == "node" and "components" in item[3] for item in dataflow)


@pytest.mark.parametrize(("token", "is_keyword"), [("true", True), ("in", True), ("of", True), ("True", False)])
def test_typescript_keyword_weights(token: str, is_keyword: bool, tmp_path: Path) -> None:
    from codebleu import calc_codebleu

    (tmp_path / "typescript.txt").write_text("", encoding="utf-8")
    reference = f"{token} marker"
    prediction = f"{token} other"
    weighted = calc_codebleu([reference], [prediction], "typescript")["weighted_ngram_match_score"]
    unweighted = calc_codebleu([reference], [prediction], "typescript", keywords_dir=tmp_path)[
        "weighted_ngram_match_score"
    ]
    assert (weighted > unweighted) is is_keyword


def test_fortran_derived_array_write_does_not_assign_the_index() -> None:
    code = "program main\ntype element\ninteger :: field\nend type\ntype(element) :: a(3)\ninteger :: i=1, x=2\na(i)%field=x\nprint *, i\nend program"
    parser = Parser(get_tree_sitter_language("fortran"))
    assert not parser.parse(code.encode("utf-8")).root_node.has_error
    dataflow = get_data_flow(code, [parser, dfg_function["fortran"]])
    definitions = [item for item in dataflow if item[0] == "i" and item[2] == "computedFrom"]
    assert len(definitions) == 1
    assert definitions[0][3] == ["1"]
    assert dataflow[-1][4] == [definitions[0][1]]
