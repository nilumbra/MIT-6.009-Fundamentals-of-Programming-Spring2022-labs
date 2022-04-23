#!/usr/bin/env python3
import os
import lab
import sys
import json

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)

def make_tester(func):
    """
    Helper to wrap a function so that, when called, it produces a
    dictionary instead of its normal result.  If the function call works
    without raising an exception, then the results are included.
    Otherwise, the dictionary includes information about the exception that
    was raised.
    """
    def _tester(*args):
        try:
            return {'ok': True, 'output': func(*args)}
        except lab.CarlaeError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            return {'ok': False, 'type': exc_type.__name__}
    return _tester


def load_test_values(n):
    """
    Helper function to load test inputs/outputs
    """
    with open(os.path.join(TEST_DIRECTORY, 'test_inputs', '%02d.json' % n)) as f:
        inputs = json.load(f)
    with open(os.path.join(TEST_DIRECTORY, 'test_outputs', '%02d.json' % n)) as f:
        outputs = json.load(f)
    return inputs, outputs


def run_continued_evaluations(ins):
    """
    Helper to evaluate a sequence of expressions in an environment.
    """
    env = None
    outs = []
    t = make_tester(lab.result_and_env)
    for i in ins:
        if env is None:
            args = (i, )
        else:
            args = (i, env)
        out = t(*args)
        if out['ok']:
            env = out['output'][1]
        if out['ok']:
            if isinstance(out['output'][0], (int, float)):
                out['output'] = out['output'][0]
            else:
                out['output'] = 'SOMETHING'
        outs.append(out)
    return outs


def compare_outputs(x, y, msg):
    if x['ok']:
        assert y['ok'], msg + f'\n\nExpected an exception ({y.get("type", None)})'
        if isinstance(x['output'], (int, float)):
            assert type(x['output']) == type(y['output']), msg + f'\n\nOutput has incorrect type (expected {type(y.get("output", None))} but got {type(x.get("output", None))}'
            assert abs(x['output'] - y['output']) <= 1e-6, msg + f'\n\nOutput has incorrect value (expected {y.get("output", None)!r} but got {x.get("output", None)!r})'
        else:
            assert x['output'] == y['output'], msg + f'\n\nOutput has incorrect value (expected {y.get("output", None)!r} but got {x.get("output", None)!r})'
    else:
        assert not y['ok'], msg + f'\n\nDid not expect an exception (got {x.get("type", None)}, expected {y.get("output", None)!r})'
        assert x['type'] == y['type'], msg + f'\n\nExpected {y.get("type", None)} to be raised, not {x.get("type", None)}'
        assert x.get('when', 'eval') == y.get('when', 'eval'), msg + f'\n\nExpected error to be raised at {y.get("when", "eval")} time, not at {x.get("when", "eval")} time.'

def do_continued_evaluations(n):
    """
    Test that the results from running continued evaluations in the same
    environment match the expected values.
    """
    inp, out = load_test_values(n)
    msg = message(n)
    results = run_continued_evaluations(inp)
    for result, expected in zip(results, out):
        compare_outputs(result, expected, msg)

def do_raw_continued_evaluations(n):
    """
    Test that the results from running continued evaluations in the same
    environment match the expected values.
    """
    with open(os.path.join(TEST_DIRECTORY, 'test_outputs', '%02d.json' % n)) as f:
        expected = json.load(f)
    env = None
    results = []
    t = make_tester(lab.result_and_env)
    with open(os.path.join(TEST_DIRECTORY, 'test_inputs', '%02d.carlae' % n)) as f:
        for line in iter(f.readline, ''):
            try:
                parsed = lab.parse(lab.tokenize(line.strip()))
            except lab.CarlaeSyntaxError:
                results.append({'expression': line.strip(), 'ok': False, 'type': 'CarlaeSyntaxError', 'when': 'parse'})
                continue
            out = t(*((parsed, ) if env is None else (parsed, env)))
            if out['ok']:
                env = out['output'][1]
            if out['ok']:
                if isinstance(out['output'][0], (int, float)):
                    out['output'] = out['output'][0]
                else:
                    out['output'] = 'SOMETHING'
            out['expression'] = line.strip()
            results.append(out)
    for ix, (result, exp) in enumerate(zip(results, expected)):
        msg = f"for line {ix+1} in test_inputs/%02d.carlae:\n    {result['expression']}" % n
        compare_outputs(result, exp, msg=msg)


def run_test_number(n, func):
    tester = make_tester(func)
    inp, out = load_test_values(n)
    msg = message(n)
    for i, o in zip(inp, out):
        compare_outputs(tester(i), o, msg)

def message(n):
    msg = "\nfor test_inputs/"+str(n)+".json"
    try:
        with open(os.path.join(TEST_DIRECTORY, 'carlae_code', '%02d.carlae' % n)) as f:
            code = f.read()
        msg += " and carlae_code/"+str(n)+".carlae"
    except Exception as e:
        with open(os.path.join(TEST_DIRECTORY, 'test_inputs', '%02d.json' % n)) as f:
            code = str(json.load(f))
    msg += " that begins with\n"
    msg += code if len(code) < 80 else code[:80]+'...'
    return msg


## TESTS FOR TOKENIZATION AND PARSING

def test_tokenize():
    run_test_number(1, lab.tokenize)

def test_parse():
    run_test_number(2, lab.parse)

def test_tokenize_and_parse():
    run_test_number(3, lambda i: lab.parse(lab.tokenize(i)))


## TESTS FOR CALCULATOR


def test_calc():
    run_test_number(4, lab.evaluate)

def test_mult_div():
    run_test_number(5, lab.evaluate)


## TESTS FOR VARIABLE ASSIGNMENT AND LOOKUP

def test_simple_assignment_1():
    do_continued_evaluations(6)

def test_simple_assignment_2():
    do_continued_evaluations(7)

def test_bad_lookups():
    do_continued_evaluations(8)

def test_rename_builtin():
    do_continued_evaluations(9)


## TESTS FOR FUNCTION DEFINITION/APPLICATIONi

def test_simple_function():
    do_continued_evaluations(10)

def test_inline_lambda():
    do_continued_evaluations(11)

def test_closures():
    do_continued_evaluations(12)


## INTEGRATION TESTS

def test_short_definition():
    do_raw_continued_evaluations(13)

def test_dependent_definition():
    do_raw_continued_evaluations(14)

def test_scoping_1():
    do_raw_continued_evaluations(15)

def test_scoping_2():
    do_raw_continued_evaluations(16)

def test_scoping_3():
    do_raw_continued_evaluations(17)

def test_scoping_4():
    do_raw_continued_evaluations(18)

def test_scoping_5():
    do_raw_continued_evaluations(19)

def test_calling_errors():
    do_raw_continued_evaluations(20)

def test_functionception():
    do_raw_continued_evaluations(21)

def test_alias():
    do_raw_continued_evaluations(22)

def test_big_scoping_1():
    do_raw_continued_evaluations(23)

def test_big_scoping_2():
    do_raw_continued_evaluations(24)

def test_big_scoping_3():
    do_raw_continued_evaluations(25)

def test_big_scoping_4():
    do_raw_continued_evaluations(26)


## ADDITIONAL TESTS FOR COMMON ERRORS

def test_more_syntax():
    do_raw_continued_evaluations(27)

def test_nested_defines():
    do_raw_continued_evaluations(28)


if __name__ == '__main__':
    import os
    import sys
    import json
    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gather", action='store_true')
    parser.add_argument("--server", action='store_true')
    parser.add_argument("--initial", action='store_true')
    parser.add_argument("args", nargs="*")

    parsed = parser.parse_args()


    class TestData:
        def __init__(self, gather=False):
            self.alltests = None
            self.results = {'passed': []}
            self.gather = gather

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            if self.gather:
                self.alltests = [i.name for i in session.items]


    pytest_args = ['-v', __file__]

    if parsed.server:
        pytest_args.insert(0, '--color=yes')

    if parsed.gather:
        pytest_args.insert(0, '--collect-only')

    testinfo = TestData(parsed.gather)
    res = pytest.main(
        ['-k', ' or '.join(parsed.args), *pytest_args],
        **{'plugins': [testinfo]}
    )

    if parsed.server:
        _dir = os.path.dirname(__file__)
        if parsed.gather:
            with open(os.path.join(_dir, 'alltests.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.alltests))
                f.write('\n')
        else:
            with open(os.path.join(_dir, 'results.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.results))
                f.write('\n')
