#!/usr/bin/env python3
import os
import lab
import json

import sys
sys.setrecursionlimit(100000)

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)

bag_list = [
  { (0,0), (1,0), (2,0) },  # vertical 3x1 bag
  { (0,0), (0,1), (0,2) },  # horizontal 1x3 bag
  { (0,0), (0,1), (1,0), (1,1) }, # square bag
  { (0,0), (1,0), (1,1) },  # L-shaped bag
  { (0,0), (0,1), (1,0), (2,0), (2,1) },  # C-shaped bag
  { (0,0), (0,1), (1,1), (2,0), (2,1) },  # reverse C-shaped bag
]

def test_01():
    # horizontal bag in 1x3 tent, no rocks => fits 
    tent_size = (1,3)
    rocks = set()
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_02():
    # vertical bag in 3x1 tent, no rocks => fits 
    tent_size = (3,1)
    rocks = set()
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_03():
    # L-shaped bag in 2x2 tent, one rock => fits 
    tent_size = (2,2)
    rocks = {(0,1)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_04():
    # Square bag in 2x2 tent, no rocks => fits 
    tent_size = (2,2)
    rocks = set()
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_05():
    # 4x4 tent, no rocks => fits 
    tent_size = (4,4)
    rocks = set()
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_06():
    # C-shaped bag in 3x2 tent, one rock => fits 
    tent_size = (3,2)
    rocks = {(1,1)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_07():
    # reverse-C-shaped bag in 3x2 tent, one rock => fits 
    tent_size = (3,2)
    rocks = {(1,0)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_08():
    # 7x3 tent, one rock => fits 
    tent_size = (7,3)
    rocks = {(1,1)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_09():
    # 3x6 tent, three rocks => fits 
    tent_size = (3,6)
    rocks = {(2,1),(0,4),(1,4)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_10():
    # 5x2 tent, two rocks => fits 
    tent_size = (5,2)
    rocks = {(1,0),(3,1)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_11():
    # 5x5 tent with two rocks in the center 
    tent_size = (5,5)
    rocks = {(2,2),(2,3)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_12():
    # 5x5 tent with 4 rocks => fails 
    tent_size = (5,5)
    rocks = {(1,1),(1,3),(3,1),(3,3)}
    packable = False
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_13():
    # 5x5 tent with three rocks => fits 
    tent_size = (5,5)
    rocks = {(1,1),(1,3),(3,1)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_14():
    # 9x7 tent with scattered rocks 
    tent_size = (9,7)
    rocks = {(0,2), (2,2), (2,4), (3,4), (7,4), (5,4), (5,5), (8,6), (7,1)}
    packable = True
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def test_15():
    # 7x6 tent with two rocks => fails 
    tent_size = (7,6)
    rocks = {(5,5),(6,4)}
    packable = False
    validate_result(tent_size, rocks, packable, lab.pack(tent_size, rocks, bag_list))

def validate_result(tent_size, covered, packable, result):
    if not packable:
        assert result is None, "Proposed a packing for an impossible tent!"
        return
    assert result is not None, "Failed to find a packing solution where one exists."
    assert isinstance(result, list), "Result should be a list."

    (rows,cols) = tent_size
    tent = [[0 for c in range(cols)] for r in range(rows)]
    for r,c in covered: tent[r][c] = 'r'
    for bag in result:
        btype = bag.get("shape")
        assert btype is not None, "Person dictionary missing 'shape' key."
        assert isinstance(btype, int), "Person shape not an int."
        assert btype >= 0 and btype < len(bag_list), "Person shape out of range."

        anchor = bag.get("anchor")
        assert anchor is not None, "Person dictionary missing 'anchor' key."
        assert isinstance(anchor, tuple), "Person anchor not a tuple."
        assert 2 == len(anchor), "Person anchor not length 2."
        for i in [0, 1]:
            assert isinstance(anchor[i], int), "Person anchor not of the form (int,int)."
        assert anchor[0] >= 0 and anchor[0] < rows, "Person anchor row out of range."
        assert anchor[1] >= 0 and anchor[1] < cols, "Person anchor column out of range."
            
        squares = [(anchor[0] + r, anchor[1] + c) for r,c in bag_list[btype]]
        for (r,c) in squares:
            assert r >= 0 and r < rows and c >= 0 and c < cols, "One of your sleeping bags is not in the tent: "+str(bag)
            assert "r" != tent[r][c], "Found a sleeping bag over a rock: "+str(bag)
            assert "b" != tent[r][c], "Found overlapping sleeping bag: "+str(bag)
            tent[r][c] = "b" #mark bag

    all_filled = all(tent[r][c] != 0 for c in range(cols) for r in range(rows))
    assert all_filled, "Oops, there's still an empty square"

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

        def pytest_collection_finish(self, session):
            self.results['total'] = [i.name for i in session.items]

        def pytest_unconfigure(self, config):
            print(json.dumps(self.results))

    if os.environ.get('CATSOOP'):
        args = ['--color=yes', '-v', __file__]
        if len(sys.argv) > 1:
            args = ['-k', sys.argv[1], *args]
        kwargs = {'plugins': [TestData()]}
    else:
        args = ['-v', __file__] if len(sys.argv) == 1 else ['-v', *('%s::%s' % (__file__, i) for i in sys.argv[1:])]
        kwargs = {}
    res = pytest.main(args, **kwargs)
