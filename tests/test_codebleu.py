from typing import List, Any

import pytest

from codebleu.codebleu import calc_codebleu, AVAILABLE_LANGS


@pytest.mark.parametrize(['predictions', 'references', 'codebleu'], [
    (['some rannnndom words in length more than 3'], ['def test ( ) :\n pass'], 0.25),  # 'cause data_flow is 0 and considered as 1
    (['def bar ( y , x ) :\n    a = x * x\n    return a'], ['def foo ( x ) :\n    return x'], 0.4),
    (['def foo ( x ) :\n    return x * x'], ['def bar ( x ) :\n    return x'], 0.6),
    (['def bar ( x ) :\n    return x'], ['def foo ( x ) :\n    return x'], 0.8),
    (['def foo ( x ) :\n    return x'], ['def foo ( x ) :\n    return x'], 1.0),
])
def test_simple_cases(predictions: List[Any], references: List[Any], codebleu: float) -> None:
    result = calc_codebleu(references, predictions, 'python')
    print(result)
    assert result['codebleu'] == pytest.approx(codebleu, 0.1)


@pytest.mark.parametrize(['lang'], [(l,) for l in AVAILABLE_LANGS])
def test_working_for_all_langs(lang: str) -> None:
    predictions = references = ['some matching string a couple of times']
    assert calc_codebleu(references, predictions, lang)['codebleu'] == 1.0

@pytest.mark.parametrize(['predictions', 'references', 'codebleu'], [
    (
        ['public static int Sign ( double d ) { return ( float ) ( ( d == 0 ) ? 0 : ( c < 0.0 ) ? - 1 : 1) ; }'],
        ['public static int Sign ( double d ) { return ( int ) ( ( d == 0 ) ? 0 : ( d < 0 ) ? - 1 : 1) ; }'],
        0.7238
    ),
    # (
    #     ['public static int Sign ( double c ) { return ( int ) ( ( c == 0 ) ? 0 : ( c < 0 ) ? - 1 : 1) ; }'],
    #     ['public static int Sign ( double d ) { return ( int ) ( ( d == 0 ) ? 0 : ( d < 0 ) ? - 1 : 1) ; }'],
    #     0.8397
    # ),
])
def test_code_x_glue_readme_examples(predictions: List[Any], references: List[Any], codebleu: float) -> None:
    result = calc_codebleu(references, predictions, 'java')
    print(result)
    assert result['codebleu'] == pytest.approx(codebleu, 0.01)


@pytest.mark.parametrize(['predictions', 'references', 'codebleu'], [
#     ([], [], 1.0),
#     ([], [[]], 1.0),
    (['def foo ( x ) : pass'], ['def foo ( x ) : pass'], 1.0),
    (['def foo ( x ) : pass'], [['def foo ( x ) : pass']], 1.0),
    (['def foo ( x ) : pass'], [['def bar ( x ) : pass', 'def foo ( x ) : pass']], 0.95),
    (['def foo ( x ) : pass'], [['def foo ( x ) : pass', 'def bar ( x ) : pass']], 0.95),
])
def test_input_variants(predictions: List[Any], references: List[Any], codebleu: float) -> None:
    assert calc_codebleu(references, predictions, 'python')['codebleu'] == pytest.approx(codebleu, 0.01)
