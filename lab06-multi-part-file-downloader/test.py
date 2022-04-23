#!/usr/bin/env python3
import os
import lab
import time
import pickle
import sys
import warnings

import pytest

sys.setrecursionlimit(10000)

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "test_files")
with open(os.path.join(TEST_DIRECTORY, "results"), "rb") as f:
    RESULTS = pickle.load(f)

import itertools

def test_streaming():
    assert b''.join(lab.download_file('https://hz.mit.edu/hello.txt')) == b'hello!\n'

    assert b''.join(lab.download_file('https://hz.mit.edu/hello.txt', 1)) == b'hello!\n'

    res = list(itertools.islice(lab.download_file('https://hz.mit.edu/stronger6.jpg', 2), 10))
    exp = [b'\xff\xd8', b'\xff\xe1', b'J\xd3', b'Ex', b'if', b'\x00\x00', b'II', b'*\x00', b'\x08\x00', b'\x00\x00']
    assert res == exp

    res = list(itertools.islice(lab.download_file('https://hz.mit.edu/stronger6.jpg', 10), 5))
    exp = [b'\xff\xd8\xff\xe1J\xd3Exif', b'\x00\x00II*\x00\x08\x00\x00\x00',
           b'\r\x00\x00\x01\x04\x00\x01\x00\x00\x00', b'\xc0\x0f\x00\x00\x01\x01\x04\x00\x01\x00',
           b'\x00\x00\xd0\x0b\x00\x00\x0f\x01\x02\x00']
    assert res == exp

    t = time.time()
    x1, x2 = RESULTS["test_streaming"]
    stream = lab.download_file("http://scripts.mit.edu/~6.009/lab6/test_stream.py")
    assert next(stream) == x1
    assert next(stream) == x2
    assert time.time() - t < 30, "Download took too long."


def test_behaviors():
    stream = lab.download_file(
        "http://scripts.mit.edu/~6.009/lab6/redir.py/0/fivedollars.wav"
    )
    assert b"".join(stream) == RESULTS["test_redirect"]

    with pytest.raises(lab.HTTPRuntimeError):
        stream = lab.download_file(
            "http://scripts.mit.edu/~6.009/lab6/always_error.py/"
        )
        out = b"".join(stream)
    with pytest.raises(lab.HTTPRuntimeError):
        stream = lab.download_file("http://nonexistent.mit.edu/hello.txt")
        out = b"".join(stream)

    with pytest.raises(lab.HTTPRuntimeError):
        stream = lab.download_file("http://scripts.mit.edu/~6.009/lab6/redirect2.py")
        out = b"".join(stream)

    with pytest.raises(lab.HTTPFileNotFoundError):
        stream = lab.download_file(
            "http://hz.mit.edu/some_file_that_doesnt_exist.txt"
        )
        out = b"".join(stream)


def test_manifest():
    stream = lab.download_file(
        "http://scripts.mit.edu/~6.009/lab6/redir.py/0/cat_poster.jpg.parts"
    )
    assert b"".join(stream) == b"".join(RESULTS["test_big"])

    stream = lab.download_file('http://hz.mit.edu/009_lab6/test.parts.txt', 30)
    with open(os.path.join(TEST_DIRECTORY, 'manifest_test.txt'), 'rb') as f:
        assert b''.join(stream) == f.read()

    stream = lab.download_file('http://hz.mit.edu/009_lab6/test.parts', 32)
    with open(os.path.join(TEST_DIRECTORY, 'bird.jpg'), 'rb') as f:
        assert b''.join(stream) == f.read() + b'hello!\n'

    stream = lab.download_file('http://scripts.mit.edu/~6.009/lab6/test-mn.py', 5)
    with open(os.path.join(TEST_DIRECTORY, 'bird.jpg'), 'rb') as f:
        assert b''.join(stream) == f.read() + b'hello!\n'




def test_cache():
    t = time.time()
    stream = lab.download_file(
        "http://mit.edu/6.009/www/lab6_examples/happycat.png.parts"
    )
    result = b"".join(stream)
    expected = 10 * RESULTS["test_caching.1"]
    assert result == expected
    assert time.time() - t < 15, "Test took too long."

    stream = lab.download_file(
        "http://mit.edu/6.009/www/lab6_examples/numbers.png.parts"
    )
    result = b"".join(stream)
    count = sum(i in result for i in RESULTS["test_caching.2"])
    assert count > 1

    stream = lab.download_file(
        "http://mit.edu/6.009/www/lab6_examples/numbers-cached.png.parts"
    )
    result = b"".join(stream)
    count = sum(i in result for i in RESULTS["test_caching.2"])
    assert count == 1

    stream = lab.download_file(
        "http://mit.edu/6.009/www/lab6_examples/numbers.png.parts"
    )
    result = b"".join(stream)
    count = sum(i in result for i in RESULTS["test_caching.2"])
    assert count > 1

    stream = lab.download_file(
        "http://mit.edu/6.009/www/lab6_examples/numbers-cached2.png.parts"
    )
    result = b"".join(stream)
    count = sum(i in result for i in RESULTS["test_caching.2"])
    assert count > 1


def _test_5_gen(chunk_size):
    with open(os.path.join(TEST_DIRECTORY, "test_file_sequence.input"), "rb") as f:
        inp = f.read()
    for i in range(0, len(inp), chunk_size):
        yield inp[i : i + chunk_size]
        if chunk_size == 8192 and i == 270336:
            time.sleep(5)
    yield inp[i + chunk_size :]


def test_file_sequence():
    gen = _test_5_gen(8192)
    t = time.time()
    ix = 0
    for ix, file_ in enumerate(lab.files_from_sequence(gen)):
        assert file_ == RESULTS["test_file_sequence"][ix], "File %d in the sequence was not correctly extracted." % ix
        if ix == 4:
            assert time.time() - t < 0.5, "Yielding first 5 files took too long"

    assert ix == len(RESULTS["test_file_sequence"]) - 1, "Incorrect number of files in file sequence."

    gen = _test_5_gen(2)
    t = time.time()
    ix = 0
    for ix, file_ in enumerate(lab.files_from_sequence(gen)):
        assert file_ == RESULTS["test_file_sequence"][ix], "File %d in the sequence was not correctly extracted." % ix

    gen = _test_5_gen(1_000_000_000_000)
    t = time.time()
    ix = 0
    for ix, file_ in enumerate(lab.files_from_sequence(gen)):
        assert file_ == RESULTS["test_file_sequence"][ix], "File %d in the sequence was not correctly extracted." % ix

    assert ix == len(RESULTS["test_file_sequence"]) - 1, "Incorrect number of files in file sequence."

    stream = lab.download_file('http://scripts.mit.edu/~6.009/lab6/cats-fast.png-seq.py')
    files = lab.files_from_sequence(stream)
    with open(os.path.join(TEST_DIRECTORY, 'cats-seq.pickle'), 'rb') as f:
        res = pickle.load(f)
        for ix, elt in enumerate(iter(lambda: next(files), None)):
            assert res[ix % 20] == elt
            if ix == 143:
                break



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
