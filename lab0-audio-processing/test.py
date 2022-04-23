#!/usr/bin/env python3

import os
import lab
import copy
import json
import pickle

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def compare_sounds(result, expected, eps=1e-6):
    # well formed?
    assert isinstance(result['rate'], int), 'Sampling rate should be an integer'
    assert len(result['left']) == len(result['right']), 'Left and Right channels do not have the same length'

    # matches expected?
    assert result['rate'] == expected['rate'], 'Sampling rates do not match'
    assert len(result['left']) == len(expected['left']), 'Lengths do not match'
    for ix, ((res_l, res_r), (exp_l, exp_r)) in enumerate(zip(zip(result['left'], result['right']), zip(expected['left'], expected['right']))):
        assert abs(res_l-exp_l) <= eps and abs(res_r-exp_r) < eps, f'Values at index {ix} do not match.'


def compare_against_file(x, fname):
    compare_sounds(x, lab.load_wav(fname), eps=(2/(2**15-1)))

def load_pickle_pair(name):
    with open(os.path.join(TEST_DIRECTORY, 'test_inputs', name), 'rb') as f:
        with open(os.path.join(TEST_DIRECTORY, 'test_outputs', name), 'rb') as f2:
            return (pickle.load(f), pickle.load(f2))


def test_backwards_small():
    inp = {
        'rate': 20,
        'left': [1,2,3,4,5,6],
        'right': [7,6,5,4,3,2],
    }
    inp2 = copy.deepcopy(inp)
    out = {
        'rate': 20,
        'left': [6,5,4,3,2,1],
        'right': [2,3,4,5,6,7],
    }
    compare_sounds(lab.backwards(inp), out)
    assert inp == inp2, 'be careful not to modify the input!'


def test_backwards_real():
    inp = lab.load_wav(os.path.join(TEST_DIRECTORY, 'sounds', 'hello.wav'))
    inp2 = copy.deepcopy(inp)
    outfile = os.path.join(TEST_DIRECTORY, 'test_outputs', 'hello_backwards.wav')
    compare_against_file(lab.backwards(inp), outfile)
    assert inp == inp2, 'be careful not to modify the input!'

def test_backwards_random_1():
    inps, exp = load_pickle_pair('backwards_01.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.backwards(*inps), exp)
    assert inps == inps2, 'be careful not to modify the input!'

def test_backwards_random_2():
    inps, exp = load_pickle_pair('backwards_02.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.backwards(*inps), exp)
    assert inps == inps2, 'be careful not to modify the input!'


def test_mix_small():
    s1 = {
        'rate': 30,
        'left': [1,2,3,4,5,6],
        'right': [7,6,5,4,3,2],
    }
    s2 = {
        'rate': 20,
        'left': [1,2,3,4,5,6],
        'right': [7,6,5,4,3,2],
    }
    s3 = {
        'rate': 30,
        'left': [7, 8, 9, 10],
        'right': [12, 13, 14, 15],
    }

    s4 = {
        'rate': 30,
        'left': [0.7+2.1, 1.4+2.4, 2.1+2.7, 2.8+3.0],
        'right': [4.9+3.6, 4.2+3.9, 3.5+4.2, 2.8+4.5]
    }

    assert lab.mix(s1, s2, 0.5) is None
    compare_sounds(lab.mix(s1, s3, 0.7), s4)


def test_mix_real():
    inp1 = lab.load_wav(os.path.join(TEST_DIRECTORY, 'sounds', 'chord.wav'))
    inp2 = lab.load_wav(os.path.join(TEST_DIRECTORY, 'sounds', 'crash.wav'))
    inp3 = copy.deepcopy(inp1)
    inp4 = copy.deepcopy(inp2)

    res = lab.mix(inp1, inp2, 0.35)
    outfile = os.path.join(TEST_DIRECTORY, 'test_outputs', 'chord_crash.wav')
    compare_against_file(res, outfile)

    assert inp1 == inp3, 'be careful not to modify the input!'
    assert inp2 == inp4, 'be careful not to modify the input!'


def test_mix_random_1():
    inps, exp = load_pickle_pair('mix_01.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.mix(*inps), exp)
    assert inps == inps2, 'be careful not to modify the inputs!'


def test_mix_random_2():
    inps, exp = load_pickle_pair('mix_02.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.mix(*inps), exp)
    assert inps == inps2, 'be careful not to modify the inputs!'


def test_echo_small():
    inp = {
        'rate': 9,
        'left': [1, 2, 3],
        'right': [0, 4, 0]
    }
    inp2 = copy.deepcopy(inp)
    exp = {
        'rate': 9,
        'left': [1,2,3, 0,0, 0.7,1.4,2.1, 0,0, 0.49,0.98,1.47],
        'right': [0,4,0, 0,0, 0,2.8,0, 0,0, 0,1.96,0],
    }
    compare_sounds(lab.echo(inp, 2, 0.6, 0.7), exp)
    assert inp == inp2, 'be careful not to modify the inputs!'


def test_echo_real():
    inp = lab.load_wav(os.path.join(TEST_DIRECTORY, 'sounds', 'synth.wav'))
    inp2 = copy.deepcopy(inp)
    outfile = os.path.join(TEST_DIRECTORY, 'test_outputs', 'synth_echo.wav')
    compare_against_file(lab.echo(inp, 6, 0.5, 0.7), outfile)
    assert inp == inp2, 'be careful not to modify the input!'


def test_echo_random_1():
    inps, exp = load_pickle_pair('echo_01.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.echo(*inps), exp)
    assert inps == inps2, 'be careful not to modify the inputs!'


def test_echo_random_2():
    inps, exp = load_pickle_pair('echo_02.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.echo(*inps), exp)
    assert inps == inps2, 'be careful not to modify the inputs!'


def test_pan_small():
    inp = {
        'rate': 42,
        'left': [4, 4, 4, 4, 4],
        'right': [6, 6, 6, 6, 6],
    }
    inp2 = copy.deepcopy(inp)
    exp = {
        'rate': 42,
        'left': [4, 3, 2, 1, 0],
        'right': [0, 1.5, 3, 4.5, 6],
    }
    compare_sounds(lab.pan(inp), exp)
    assert inp == inp2, 'be careful not to modify the input!'


def test_pan_real():
    inp = lab.load_wav(os.path.join(TEST_DIRECTORY, 'sounds', 'mystery.wav'))
    inp2 = copy.deepcopy(inp)
    outfile = os.path.join(TEST_DIRECTORY, 'test_outputs', 'mystery_pan.wav')
    compare_against_file(lab.pan(inp), outfile)
    assert inp == inp2, 'be careful not to modify the input!'


def test_pan_random_1():
    inps, exp = load_pickle_pair('pan_01.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.pan(*inps), exp)
    assert inps == inps2, 'be careful not to modify the input!'

def test_pan_random_2():
    inps, exp = load_pickle_pair('pan_02.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.pan(*inps), exp)
    assert inps == inps2, 'be careful not to modify the input!'


def test_remove_vocals_small():
    inp = {
        'rate': 30,
        'left': [7, 9, 3, 4],
        'right': [12, 2, 9, 2],
    }
    inp2 = copy.deepcopy(inp)
    exp = {
        'rate': 30,
        'left': [-5, 7, -6, 2],
        'right': [-5, 7, -6, 2],
    }
    compare_sounds(lab.remove_vocals(inp), exp)
    assert inp == inp2, 'be careful not to modify the input!'


def test_remove_vocals_random_1():
    inps, exp = load_pickle_pair('remove_vocals_01.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.remove_vocals(*inps), exp)
    assert inps == inps2, 'be careful not to modify the input!'

def test_remove_vocals_random_2():
    inps, exp = load_pickle_pair('remove_vocals_02.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.remove_vocals(*inps), exp)
    assert inps == inps2, 'be careful not to modify the input!'

def test_remove_vocals_random_3():
    inps, exp = load_pickle_pair('remove_vocals_03.pickle')
    inps2 = copy.deepcopy(inps)
    compare_sounds(lab.remove_vocals(*inps), exp)
    assert inps == inps2, 'be careful not to modify the input!'

if __name__ == '__main__':
    import sys
    import json

    class TestData:
        def __init__(self):
            self.results = {'passed': []}

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_modifyitems(self, items):
            self.results['total'] = [i.name for i in items]

        def pytest_unconfigure(self, config):
            print(json.dumps(self.results))

    args = ['-v', __file__] if len(sys.argv) == 1 else ['-v', *('%s::%s' % (__file__, i) for i in sys.argv[1:])]
    if os.environ.get('CATSOOP'):
        args.insert(0, '--color=yes')
    kwargs = {'plugins': [TestData()]} if os.environ.get('CATSOOP') else {}
    res = pytest.main(args, **kwargs)
