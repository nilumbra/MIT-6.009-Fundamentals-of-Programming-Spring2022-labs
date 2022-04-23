#!/usr/bin/env python3
import os
import lab
import json
import copy

import pytest

import sys
sys.setrecursionlimit(10000)

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_inputs')

## HELPER FUNCTIONS

def _open_case(casename):
    with open(os.path.join(TEST_DIRECTORY, casename + ".json")) as f:
        cnf = json.load(f)
        res = [[(variable, polarity)
                 for variable, polarity in clause]
                for clause in cnf]
        rev = [[(variable, polarity)
                 for variable, polarity in clause[::-1]]
                for clause in cnf]
        rev_f = sorted(rev)
        s_f = res[::-1]
        s_f_2 = sorted(res, key=len)
        return res, rev, rev_f, s_f, s_f_2

def _satisfiable(cnf):
    assignment = lab.satisfying_assignment(copy.deepcopy(cnf))
    assert all(any(variable in assignment and assignment[variable] == polarity
                   for variable, polarity in clause)
               for clause in cnf)


def _unsatisfiable(cnf):
    assignment = lab.satisfying_assignment(copy.deepcopy(cnf))
    assert assignment is None


def _test_from_file(casename, testfunc):
    for cnf in _open_case(casename):
        testfunc(cnf)


## TESTS FOR SAT SOLVER

def test_sat_small_nested_backtrack():
    cnf = [[("a",True), ("b",True)], [("a",False), ("b",False), ("c",True)],
           [("b",True),("c",True)], [("b",True),("c",False)]]
    _satisfiable(cnf)

def test_sat_small_double_backtrack():
    # a will be guessed as True, which is wrong
    # then a both assignments on b will fail and cause a backtrack to a
    cnf = [[("a",True),("b",True)], [("a",False),("b",False),("c",True)], [("b",True),("c",True)], [("b",True),("c",False)], [("a",False),("b",False),("c",False)]]
    _satisfiable(cnf)

def test_sat_small_deep_double_backtrack():
    # a will be guessed as True, which is wrong
    # then a both assignments on b will fail and cause a backtrack to a
    cnf = [[("d",True),("b",True)],[("a",True),("b",True)], [("a",False),("b",False),("c",True)], [("b",True),("c",True)], [("b",True),("c",False)], [("a",False),("b",False),("c",False)]]
    _satisfiable(cnf)

def test_sat_small_deep_double_backtrack2():
    cnf = [[("d",True),("b",True)],[("a",False),("b",True)], [("a",True),("b",False),("c",True)], [("b",True),("c",True)], [("b",True),("c",False)], [("a",True),("b",False),("c",False)]]
    _satisfiable(cnf)

def test_sat_big_A():
    _test_from_file('A', _satisfiable)

def test_sat_big_B():
    _test_from_file('B', _satisfiable)

def test_sat_big_C():
    _test_from_file('C', _satisfiable) # irrelevancies

def test_sat_big_D():
    _test_from_file('D', _unsatisfiable)

def test_sat_big_E():
    _test_from_file('E', _unsatisfiable)

def test_sat_big_F():
    _test_from_file('F', _satisfiable)

def test_sat_big_G():
    _test_from_file('G', _unsatisfiable)

def test_sat_big_H():
    _test_from_file('H', _satisfiable)

def test_sat_big_I():
    _test_from_file('I', _satisfiable)


# These three tests use your satisfying_assignment code to solve sudoku
# puzzles (formulated as Boolean formulas).
#
# See http://www.cs.qub.ac.uk/~I.Spence/SuDoku/SuDoku.html for one
# explanation of how to formulate a CNF formula for a sudoku puzzle.


def _get_sudoku(n):
    with open(os.path.join(TEST_DIRECTORY, 'sudoku%s.json' % n)) as f:
        return [[tuple(literal) for literal in clause] for clause in json.loads(f.read())]


def _run_sudoku_test(n, original):
    result = lab.satisfying_assignment(_get_sudoku(n))
    assert result is not None, "There is a valid sudoku solution, but your code returned None."
    _check_sudoku(original, _assignment_to_grid(result))


def _assignment_to_grid(a):
    a = {k for k,v in a.items() if v}
    out = []
    for r in range(9):
        row = []
        for c in range(9):
            row.append([v+1 for v in range(9) if '%s_%s_%s' % (r, c, v) in a][0])
        out.append(row)
    return out


def _get_superblock(sr, sc):
    return {(r, c) for r in range(sr*3, (sr+1)*3) for c in range(sc*3, (sc+1)*3)}


def _check_sudoku(original, result):
    all_nums = set(range(1, 10))

    # all values from original must be preserved
    assert all((iv==jv or iv == 0) for i,j in zip(original, result) for iv, jv in zip(i, j))

    # all rows must contain the right values
    assert all(set(i) == all_nums for i in result)

    # all columns must contain the right values
    for c in range(9):
        assert set(i[c] for i in result) == all_nums

    # all superblocks must contain the right values
    for sr in range(3):
        for sc in range(3):
            assert set(result[r][c] for r, c in _get_superblock(sr, sc)) == all_nums


def test_sat_sudoku1():
    """
    sudoku corresponding to the following board (0 denotes empty)
    """
    original = [[5,1,7,6,0,0,0,3,4],
                [2,8,9,0,0,4,0,0,0],
                [3,4,6,2,0,5,0,9,0],
                [6,0,2,0,0,0,0,1,0],
                [0,3,8,0,0,6,0,4,7],
                [0,0,0,0,0,0,0,0,0],
                [0,9,0,0,0,0,0,7,8],
                [7,0,3,4,0,0,5,6,0],
                [0,0,0,0,0,0,0,0,0]]
    _run_sudoku_test(1, original)


def test_sat_sudoku2():
    """
    sudoku corresponding to the following board (0 denotes empty)
    """
    original = [[5,1,7,6,0,0,0,3,4],
                [0,8,9,0,0,4,0,0,0],
                [3,0,6,2,0,5,0,9,0],
                [6,0,0,0,0,0,0,1,0],
                [0,3,0,0,0,6,0,4,7],
                [0,0,0,0,0,0,0,0,0],
                [0,9,0,0,0,0,0,7,8],
                [7,0,3,4,0,0,5,6,0],
                [0,0,0,0,0,0,0,0,0]]
    _run_sudoku_test(2, original)


def test_sat_sudoku3():
    """
    sudoku corresponding to the following board (0 denotes empty)
    (from http://www.extremesudoku.info/sudoku.html)
    """
    original = [[0,0,1,0,0,9,0,0,3],
                [0,8,0,0,2,0,0,9,0],
                [9,0,0,1,0,0,8,0,0],
                [1,0,0,5,0,0,4,0,0],
                [0,7,0,0,3,0,0,5,0],
                [0,0,6,0,0,4,0,0,7],
                [0,0,8,0,0,5,0,0,6],
                [0,3,0,0,7,0,0,4,0],
                [2,0,0,3,0,0,9,0,0]]
    _run_sudoku_test(3, original)


## TESTS FOR SCHEDULING

def _open_scheduling_case(casename):
    with open(os.path.join(TEST_DIRECTORY, casename + ".json")) as f:
        v = json.load(f)
        return ({p[0] : p[1]
                 for p in v[0].items()}, v[1])


def _scheduling_satisfiable(casename=None, students=None, sessions=None):
    if casename is not None:
        students, sessions = _open_scheduling_case(casename)
    formula = lab.boolify_scheduling_problem(copy.deepcopy(students),
                                                  copy.deepcopy(sessions))
    sched = lab.satisfying_assignment(formula)
    assert sched is not None

    unplaced_students = set(students)

    for var, val in sched.items():
        if val:
            student, session = var.split('_')

            assert student in unplaced_students, "Students should be assigned at most one session."
            unplaced_students.remove(student)

            assert student in students, "This is not a valid student."
            assert session in sessions, "This is not a valid session."

            assert session in students[student], "Student should be assigned a desired session."

            assert sessions[session] >= 1, "This session is over-capacity."
            sessions[session] -= 1

    assert not unplaced_students, "Some students were not placed into a section!"


def _scheduling_unsatisfiable(casename):
    students, sessions = _open_scheduling_case(casename)
    sched = lab.satisfying_assignment(
        lab.boolify_scheduling_problem(copy.deepcopy(students),
                                            copy.deepcopy(sessions)))
    assert sched is None

def test_scheduling_small():
    student_preferences = {"Alice": ["session1", "session2"], "Bob": ["session3"], "Charles": ["session3"]}
    room_capacities = {"session1": 1, "session2": 1, "session3": 3}
    _scheduling_satisfiable(None, student_preferences, room_capacities)


def test_scheduling_small_2():
    student_preferences = {"student0": ["session1", "session0"], "student1": ["session1", "session2"], "student2": ["session2"]}
    room_capacities = {"session0": 2, "session2": 2, "session1": 1}
    _scheduling_satisfiable(None, student_preferences, room_capacities)

def test_scheduling_A():
    _scheduling_satisfiable('A_Sat')

def test_scheduling_B():
    _scheduling_satisfiable('B_Sat')

def test_scheduling_C():
    _scheduling_unsatisfiable('C_Unsat')

def test_scheduling_D():
    _scheduling_satisfiable('D_Sat')

def test_scheduling_E():
    _scheduling_unsatisfiable('E_Unsat')


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
