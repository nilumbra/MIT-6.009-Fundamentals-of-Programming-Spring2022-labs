#!/usr/bin/env python3
import os
import ast
import types
import pytest

import mixtape

TEST_DIRECTORY = os.path.dirname(__file__)

def _test_valid(songs, target, result):
    assert len(result) == len(set(result)), 'no duplicates allowed!'
    assert all(s in songs for s in result), 'only valid songs should be included!'
    assert sum(songs[i] for i in result) == target, 'incorrect duration!'

def test_mixtape_examples():
    songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
    _test_valid(songs, 11, mixtape.mixtape(dict(songs), 11))
    assert mixtape.mixtape(dict(songs), 1000) == None
    _test_valid(songs, 21, mixtape.mixtape(dict(songs), 21))

@pytest.mark.parametrize('n', list(range(1, 26)))
def test_mixtape_from_file(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'songs_%02d.py' % n), 'r') as f:
        (songs, target, valid) = ast.literal_eval(f.read())
    result = mixtape.mixtape(dict(songs), target)
    if valid:
        assert result is not None
        _test_valid(songs, target, result)
    else:
        assert result is None
