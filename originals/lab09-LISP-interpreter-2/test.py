#!/usr/bin/env python3
import os
import lab
import sys
import json

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)

class NotImplemented:
    def __eq__(self, other):
        return False

try:
    nil_rep = lab.result_and_env(lab.parse(['nil']))[0]
except:
    nil_rep = NotImplemented()


def list_from_ll(ll):
    if isinstance(ll, lab.Pair):
        if ll.tail == nil_rep:
            return [list_from_ll(ll.head)]
        return [list_from_ll(ll.head)] + list_from_ll(ll.tail)
    elif ll == nil_rep:
        return []
    elif isinstance(ll, (float, int)):
        return ll
    else:
        return 'SOMETHING'

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
    try:
        t = make_tester(lab.result_and_env)
    except:
        t = make_tester(lab.evaluate)
    for i in ins:
        if env is None:
            args = (i, )
        else:
            args = (i, env)
        out = t(*args)
        if out['ok']:
            env = out['output'][1]
        if out['ok']:
            try:
                typecheck = (int, float, lab.Pair)
                func = list_from_ll
            except:
                typecheck = (int, float)
                func = lambda x: x if isinstance(x, typecheck) else 'SOMETHING'
            out['output'] = func(out['output'][0])
        outs.append(out)
    return outs

def compare_outputs(x, y, msg):
    if x['ok']:
        assert y['ok'], msg + f'\n\nExpected an exception ({y.get("type", None)}), but got {x.get("output", None)!r}'
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
    try:
        t = make_tester(lab.result_and_env)
    except:
        t = make_tester(lab.evaluate)
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
                try:
                    typecheck = (int, float, lab.Pair)
                    func = list_from_ll
                except:
                    typecheck = (int, float)
                    func = lambda x: x if isinstance(x, typecheck) else 'SOMETHING'
                out['output'] = func(out['output'][0])
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


def _test_file(fname, num):
    try:
        out = lab.evaluate_file(os.path.join(TEST_DIRECTORY, 'test_files', fname))
        out = list_from_ll(out)
        out = {'ok': True, 'output': out}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        out = {'ok': False, 'type': exc_type.__name__}
    with open(os.path.join(TEST_DIRECTORY, 'test_outputs', f'{num}.json')) as f:
        expected = json.load(f)
    msg = _test_file_msg(fname, num)
    return out, expected, msg


def _test_file_msg(fname, n):
    msg = "\nwhile running test_files/"+fname+" that begins with\n"
    with open(os.path.join(TEST_DIRECTORY, 'test_files', fname)) as f:
        code = f.read()
    msg += code if len(code) < 80 else code[:80]+'...'
    return msg



def test_oldbehaviors():
    run_test_number(1, lab.tokenize)
    run_test_number(2, lab.parse)
    run_test_number(3, lambda i: lab.parse(lab.tokenize(i)))
    run_test_number(4, lab.evaluate)
    run_test_number(5, lab.evaluate)
    do_continued_evaluations(6)
    do_continued_evaluations(7)
    do_continued_evaluations(8)
    do_continued_evaluations(9)
    do_continued_evaluations(10)
    do_continued_evaluations(11)
    do_continued_evaluations(12)
    do_raw_continued_evaluations(13)
    do_raw_continued_evaluations(14)
    do_raw_continued_evaluations(15)
    do_raw_continued_evaluations(16)
    do_raw_continued_evaluations(17)
    do_raw_continued_evaluations(18)
    do_raw_continued_evaluations(19)
    do_raw_continued_evaluations(20)
    do_raw_continued_evaluations(21)
    do_raw_continued_evaluations(22)
    do_raw_continued_evaluations(23)
    do_raw_continued_evaluations(24)
    do_raw_continued_evaluations(25)
    do_raw_continued_evaluations(26)
    do_raw_continued_evaluations(27)
    do_raw_continued_evaluations(28)


def test_conditionals():
    do_raw_continued_evaluations(30)

def test_comparisons():
    do_raw_continued_evaluations(76)

def test_func():
    do_raw_continued_evaluations(31)

def test_and():
    do_raw_continued_evaluations(32)

def test_or():
    do_raw_continued_evaluations(33)

def test_not():
    do_raw_continued_evaluations(34)

def test_shortcircuit_1():
    do_raw_continued_evaluations(35)

def test_shortcircuit_2():
    do_raw_continued_evaluations(36)

def test_shortcircuit_3():
    do_raw_continued_evaluations(37)

def test_shortcircuit_4():
    do_raw_continued_evaluations(38)

def test_conditional_scoping():
    do_raw_continued_evaluations(39)

def test_conditional_scoping_2():
    do_raw_continued_evaluations(40)


def test_pair_lists():
    do_raw_continued_evaluations(41)

def test_head_tail():
    do_raw_continued_evaluations(42)

def test_head_tail_2():
    do_raw_continued_evaluations(43)

def test_islist():
    do_raw_continued_evaluations(77)

def test_length():
    do_raw_continued_evaluations(44)

def test_indexing():
    do_raw_continued_evaluations(45)

def test_concat():
    do_raw_continued_evaluations(46)

def test_list_ops():
    do_raw_continued_evaluations(47)

def test_map_builtin():
    do_raw_continued_evaluations(48)

def test_map_carlaefunc():
    do_raw_continued_evaluations(49)

def test_filter_builtin():
    do_raw_continued_evaluations(50)

def test_filter_carlaefunc():
    do_raw_continued_evaluations(51)

def test_reduce_builtin():
    do_raw_continued_evaluations(52)

def test_reduce_carlaefunc():
    do_raw_continued_evaluations(53)

def test_map_filter_reduce():
    do_raw_continued_evaluations(54)

def test_begin():
    do_raw_continued_evaluations(55)


def test_file():
    compare_outputs(*_test_file("small_test1.carlae", 56))

def test_file_2():
    compare_outputs(*_test_file("small_test2.carlae", 57))

def test_file_3():
    compare_outputs(*_test_file("small_test3.carlae", 58))

def test_file_4():
    compare_outputs(*_test_file("small_test4.carlae", 59))

def test_file_5():
    compare_outputs(*_test_file("small_test5.carlae", 60))

def test_del():
    do_raw_continued_evaluations(61)

def test_let():
    do_raw_continued_evaluations(62)

def test_let_2():
    do_raw_continued_evaluations(63)

def test_let_3():
    do_raw_continued_evaluations(64)

def test_setbang():
    do_raw_continued_evaluations(65)

def test_begin2():
    do_raw_continued_evaluations(66)


def test_deep_nesting_1():
    do_raw_continued_evaluations(67)

def test_deep_nesting_2():
    do_raw_continued_evaluations(68)

def test_deep_nesting_3():
    do_raw_continued_evaluations(69)


def test_counters_oop():
    do_raw_continued_evaluations(70)

def test_fizzbuzz():
    do_raw_continued_evaluations(71)

def test_primes():
    do_raw_continued_evaluations(72)

def test_averages_oop():
    do_raw_continued_evaluations(73)

def test_nd_mines():
    do_raw_continued_evaluations(74)

def test_sudoku_solver():
    do_raw_continued_evaluations(75)


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
