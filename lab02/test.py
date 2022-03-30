#!/usr/bin/env python3
import os
import sys
import copy
import json
import pickle

import lab

sys.setrecursionlimit(10000)

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)

def compare_boards(your_board, expected_board):
    if len(your_board) != len(expected_board):
        return f"board had wrong size"
    for rn, (your_row, expected_row) in enumerate(zip(your_board, expected_board)):
        if len(your_row) != len(expected_row):
            return  f"row {rn} had wrong size"
        for cn, (your_cell, expected_cell) in enumerate(zip(your_row, expected_row)):
            if sorted(your_cell) != sorted(expected_cell):
                return f"objects at location ({rn},{cn}) don't match"


def compare_simulation(filename):
    with open(os.path.join(TEST_DIRECTORY, "test_levels", f"{filename}.json")) as f:
        level = json.load(f)
    with open(os.path.join(TEST_DIRECTORY, "test_inputs", f"{filename}.txt")) as f:
        inputs = f.read().strip().splitlines(False)
    with open(os.path.join(TEST_DIRECTORY, "test_outputs", f"{filename}.pickle"), "rb") as f:
        outputs = pickle.load(f)
    assert len(inputs) == len(outputs) != 0

    game = lab.new_game(copy.deepcopy(level))
    err_msg = compare_boards(lab.dump_game(game), level)
    if err_msg is not None:
        assert False, f"Unexpected results at setup: {err_msg}"
    for ix, (direction, (exp_dump, exp_win)) in enumerate(zip(inputs, outputs)):
        original_game = copy.deepcopy(game)
        new_game = lab.step_game(game, direction)
        assert original_game == game, "be careful not to modify the input game!"
        game = new_game
        err_msg = compare_boards(lab.dump_game(game), exp_dump)
        if err_msg is not None:
            original_dump = json.dumps(lab.dump_game(original_game))
            assert False, f"Unexpected results in step {ix}, moving {direction} starting from the following board ({err_msg}):\n\n{original_dump}\n\nYou can copy/paste this representation into the GUI to test."
        original_game = copy.deepcopy(game)
        original_dump = json.dumps(lab.dump_game(original_game))
        win = lab.victory_check(game)
        assert original_game == game, "be careful not to modify the input game!"
        assert lab.victory_check(game) == exp_win, f"Incorrect victory check in step {ix} for the following board (expected {exp_win}):\n\n{original_dump}\n\nYou can copy/paste this representation into the GUI to test."

unit_test_cases = [
    i.rsplit(".", 1)[0]
    for i in sorted(os.listdir(os.path.join(TEST_DIRECTORY, "test_levels")))
]
unit_test_cases = filter(lambda x: x[:len("unit_")] == "unit_",unit_test_cases)
print(unit_test_cases)
@pytest.mark.parametrize('test', unit_test_cases)
def test_units(test):
    compare_simulation(test)


@pytest.mark.parametrize('test_num', range(12))
def test_win(test_num):
    compare_simulation('win_%04d' % test_num)


@pytest.mark.parametrize('test_group', range(10))
def test_random(test_group):
    for i in range(10):
        compare_simulation('random_%04d' % (test_group*10 + i))


SOLVER_TEST_GROUPS = {
    'small': ['m1_044', 'm1_001', 'm1_009', 'm2_002', 'm1_021', 'm2_007', 'm1_014', 'm1_056', 'm1_002', 'm1_015', 't_001', 't_002'],
    'small2': ['m1_046', 'm2_011', 'm1_023', 'm1_003', 'm2_001', 'm2_006', 'm1_027', 'm2_005', 'm1_012', 'm1_019'],
    'small3': ['m1_051', 'm1_028', 'm1_024', 'm2_003', 'm2_010', 'm1_154', 'm1_067', 'm1_057', 'm1_055', 'm1_008'],
    'small4': ['m1_050', 'm1_011', 'm1_038', 'm1_020', 'm1_010', 'm1_030', 'm1_018', 'm1_063', 'm1_017', 'm2_020'],
    'small5': ['m1_039', 'm2_004', 'm2_017', 'm2_009', 'm1_031', 'm2_041', 'm1_032', 'm1_022', 'm1_047', 'm1_040'],
    'small6': ['m2_021', 'm1_029', 'm2_015', 'm2_022', 'm1_045', 'm1_025', 'm2_014', 'm2_039', 'm1_058', 'm1_082'],
    'small7': ['m2_018', 'm1_026', 'm2_008', 'm2_056', 'm1_013', 'm2_019', 'm2_053', 'm1_042', 'm1_004', 'm2_028', 'm2_024', 'm1_068', 'm2_029', 'm1_079', 'm2_052', 'm2_023', 'm1_041'],
    'medium': ['m1_061', 'm1_037', 'm1_071', 'm1_043', 'm1_033', 'm1_155', 'm2_133', 'm1_053', 'm2_013', 'm2_040'],
    'medium2': ['m1_081', 'm2_036', 'm2_016', 'm2_042', 'm2_038', 'm1_091', 'm1_104', 'm1_103', 'm1_006', 'm2_012'],
    'medium3': ['m2_033', 'm1_048', 'm1_119', 'm2_132', 'm1_073', 'm2_037', 'm2_025', 'm2_059', 'm2_049', 'm1_016'],
    'large': ['m2_089', 'm2_134'],
}

SOLUTION_LENGTHS = {
    'small': [1, 33, 30, 27, 17, 47, 51, 23, 16, 37, None, 0],
    'small2': [47, 39, 56, 41, 44, 55, 50, 61, 49, 41],
    'small3': [34, 33, 35, 46, 23, 429, 37, 60, 64, 97],
    'small4': [76, 78, 37, 50, 89, 21, 71, 101, 25, 46],
    'small5': [85, 61, 40, 32, 17, 77, 35, 47, 83, 20],
    'small6': [106, 104, 40, 94, 45, 29, 29, 76, 44, 52],
    'small7': [71, 41, 40, 89, 52, 75, 65, 47, 23, 42, 139, 98, 51, 48, 46, 120, 50],
    'medium': [100, 71, 120, 61, 41, 282, 618, 37, 75, 49],
    'medium2': [46, 83, 80, 107, 79, 45, 79, 35, 107, 87],
    'medium3': [98, 64, 131, 487, 102, 122, 34, 107, 30, 100],
    'large': [67, 5037]
}


def compare_solution(filename, solution):
    with open(os.path.join(TEST_DIRECTORY, "puzzles", f"{filename}.json")) as f:
        level = json.load(f)

    game = lab.new_game(level)
    for ix, direction in enumerate(solution):
        game = lab.step_game(game, direction)
        if ix != len(solution) - 1:
            assert not lab.victory_check(game)
    assert lab.victory_check(game)


@pytest.mark.parametrize('test_group', list(SOLVER_TEST_GROUPS))
def test_solver(test_group):
    assert len(SOLVER_TEST_GROUPS[test_group]) == len(SOLUTION_LENGTHS[test_group])
    for puzzle, elen in zip(SOLVER_TEST_GROUPS[test_group], SOLUTION_LENGTHS[test_group]):
        with open(os.path.join(TEST_DIRECTORY, "puzzles", f"{puzzle}.json")) as f:
            level = json.load(f)
        result = lab.solve_puzzle(lab.new_game(level))
        if elen is None:
            assert result is None, f"Expected no solution for {puzzle}, but got one."
        else:
            assert result is not None, f"Expected a solution for {puzzle}, got None."
            assert len(result) == elen, f"Expected a solution of length {elen} for {puzzle}, got {len(result)}."
            compare_solution(puzzle, result)


if __name__ == "__main__":
    import os
    import sys
    import json
    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gather", action="store_true")
    parser.add_argument("--server", action="store_true")
    parser.add_argument("--initial", action="store_true")
    parser.add_argument("args", nargs="*")

    parsed = parser.parse_args()

    class TestData:
        def __init__(self, gather=False):
            self.alltests = None
            self.results = {"passed": []}
            self.gather = gather

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != "call":
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            if self.gather:
                self.alltests = [i.name for i in session.items]

    pytest_args = ["-v", __file__]

    if parsed.server:
        pytest_args.insert(0, "--color=yes")

    if parsed.gather:
        pytest_args.insert(0, "--collect-only")

    testinfo = TestData(parsed.gather)
    res = pytest.main(
        ["-k", " or ".join(parsed.args), *pytest_args], **{"plugins": [testinfo]}
    )

    if parsed.server:
        _dir = os.path.dirname(__file__)
        if parsed.gather:
            with open(
                os.path.join(_dir, "alltests.json"), "w" if parsed.initial else "a"
            ) as f:
                f.write(json.dumps(testinfo.alltests))
                f.write("\n")
        else:
            with open(
                os.path.join(_dir, "results.json"), "w" if parsed.initial else "a"
            ) as f:
                f.write(json.dumps(testinfo.results))
                f.write("\n")
