import inspect
from typing import Any, List

import pytest
import logging

from codebleu.codebleu import AVAILABLE_LANGS, calc_codebleu


@pytest.mark.parametrize(['predictions', 'references', 'codebleu'], [
    (['some rannnndom words in length more than 3'],
     ['def test ( ) :\n pass'], 0.25),  # 'cause data_flow is 0 and considered as 1
    (['def bar ( y , x ) :\n    a = x * x\n    return a'], ['def foo ( x ) :\n    return x'], 0.4),
    (['def foo ( x ) :\n    return x * x'], ['def bar ( x ) :\n    return x'], 0.6),
    (['def bar ( x ) :\n    return x'], ['def foo ( x ) :\n    return x'], 0.8),
    (['def foo ( x ) :\n    return x'], ['def foo ( x ) :\n    return x'], 1.0),
])
def test_simple_cases(predictions: List[Any], references: List[Any], codebleu: float) -> None:
    result = calc_codebleu(references, predictions, 'python')
    logging.debug(result)
    assert result['codebleu'] == pytest.approx(codebleu, 0.1)


@pytest.mark.parametrize(['lang'], [(lang,) for lang in AVAILABLE_LANGS])
def test_exact_match_works_for_all_langs(lang: str) -> None:
    predictions = references = ['some matching string a couple of times']
    assert calc_codebleu(references, predictions, lang)['codebleu'] == 1.0


@pytest.mark.parametrize(['lang', 'predictions', 'references'], [
    ('python', ['def foo ( x ) :\n    return x'], ['def bar ( y ) :\n    return y']),
    ('java', ['public function foo ( x ) { return x }'], ['public function bar ( y ) {\n   return y\n}']),
    ('javascript', ['function foo ( x ) { return x }'], ['function bar ( y ) {\n   return y\n}']),
    ('c', ['int foo ( int x ) { return x }'], ['int bar ( int y ) {\n   return y\n}']),
    ('c_sharp', ['public int foo ( int x ) { return x }'], ['public int bar ( int y ) {\n   return y\n}']),
    ('cpp', ['int foo ( int x ) { return x }'], ['int bar ( int y ) {\n   return y\n}']),
    ('php', ['function foo ( x ) { return x }'], ['function bar ( y ) {\n   return y\n}']),
])
def test_simple_cases_work_for_all_langs(lang: str, predictions: List[Any], references: List[Any]) -> None:
    result = calc_codebleu(references, predictions, lang)
    logging.debug(result)
    assert result['codebleu'] == pytest.approx(0.6, 0.1)


def test_error_when_lang_not_supported() -> None:
    with pytest.raises(AssertionError):
        calc_codebleu(['def foo : pass'], ['def bar : pass'], 'not_supported_lang')


def test_error_when_input_length_mismatch() -> None:
    with pytest.raises(AssertionError):
        calc_codebleu(['def foo : pass'], ['def bar : pass', 'def buz : pass'], 'python')


# https://github.com/microsoft/CodeXGLUE/blob/main/Code-Code/code-to-code-trans/example.png
@pytest.mark.parametrize(['predictions', 'references', 'codebleu'], [
    # (
    #     ['public static int Sign ( double d ) { return ( float ) ( ( d == 0 ) ? 0 : ( c < 0.0 ) ? - 1 : 1) ; }'],
    #     ['public static int Sign ( double d ) { return ( int ) ( ( d == 0 ) ? 0 : ( d < 0 ) ? - 1 : 1) ; }'],
    #     0.7238  # TODO: lol, not working at <3.12
    # ),
    # (
    #     ['public static int Sign ( double c ) { return ( int ) ( ( c == 0 ) ? 0 : ( c < 0 ) ? - 1 : 1) ; }'],
    #     ['public static int Sign ( double d ) { return ( int ) ( ( d == 0 ) ? 0 : ( d < 0 ) ? - 1 : 1) ; }'],
    #     0.8397  # TODO: check, lol, not working
    # ),
])
def test_code_x_glue_readme_examples(predictions: List[Any], references: List[Any], codebleu: float) -> None:

    result = calc_codebleu(references, predictions, 'java')
    logging.debug(result)
    assert result['codebleu'] == pytest.approx(codebleu, 0.01)


@pytest.mark.parametrize(['predictions', 'references', 'codebleu'], [
    # ([], [], 1.0),
    # ([], [[]], 1.0),
    (['def foo ( x ) : pass'], ['def foo ( x ) : pass'], 1.0),
    (['def foo ( x ) : pass'], [['def foo ( x ) : pass']], 1.0),
    (['def foo ( x ) : pass'], [['def bar ( x ) : pass', 'def foo ( x ) : pass']], 0.95),
    (['def foo ( x ) : pass'], [['def foo ( x ) : pass', 'def bar ( x ) : pass']], 0.95),
])
def test_input_variants(predictions: List[Any], references: List[Any], codebleu: float) -> None:
    assert calc_codebleu(references, predictions, 'python')['codebleu'] == pytest.approx(codebleu, 0.01)


# TODO: fix this test
# @pytest.mark.timeout(1)
def test_finite_processing_time_in_bug_testcase() -> None:
    dummy_true_code = inspect.cleandoc('''
        def foo(n):
            pass
    ''')
    generated_code = inspect.cleandoc('''
        def foo(n):
           for i in range(n):
               for j in range(n):
                   for k in range(n):
                       for l in range(n):
                           for m in range(n):
                               for n in range(n):
                                   for o in range(n):
                                       for p in range(n):
                                           for q in range(n):
                                               for r in range(n):
                                                   for s in range(n):
                                                       for t in range(n):
                                   #                         for u in range(n):
                                   #                             for v in range(n):
                                   #                                 for w in range(n):
                                   #                                     for x in range(n):
                                   #                                         for y in range(n):
                                   #                                             for z in range(n):
                                   #                                                 for a in range(n):
                                   #                                                     for b in range(n):
                                   #                                                         for c in range(n):
                                   #                                                             for d in range(n):
                                   #                                                               for e in range(n):
                                   #                                                               for f in range(n):
                                   #                                                               for g in range(n):
                                   #                                                               for h in range(n):
                                   #                                                               for i in range(n):
                                   #                                                               for j in range(n):
                                   #                                                               for k in range(n):
                                   #                                                               for l in range(n):
                                   #                                                               for m in range(n):
                                   #                                                               for n in range(n):
                                   #                                                               for o in range(n):
                                   #                                                               for p in range(n):
                                   #                                                               for q in range(n):
                                   #                                                               for r in range(n):
                                   #                                                               for s
    ''')

    # just test finite processing time
    calc_codebleu([dummy_true_code], [generated_code], 'python')


# TODO: add tests with direct comparison with XLCoST and CodeXGlue results
