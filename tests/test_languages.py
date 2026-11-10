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
