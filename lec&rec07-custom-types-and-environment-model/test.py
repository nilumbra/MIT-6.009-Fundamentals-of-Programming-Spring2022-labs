#!/usr/bin/env python3
import os
import lab
import pickle
import pytest

from test_utils import safe_eval

TEST_DIRECTORY = os.path.dirname(__file__)

def symbol_rep(x):
    if isinstance(x, lab.BinOp):
        try:
            opts = (lab.Sub, lab.Div, lab.Pow)
        except:
            opts = (lab.Sub, lab.Div,)

        if isinstance(x, (lab.Add, lab.Mul)):  # commutative operations
            op_rep = frozenset
        elif isinstance(x, opts):
            op_rep = tuple
        else:
            raise NotImplementedError('No support for %s' % x.__class__.__name__)
        return (x.__class__.__name__, op_rep(symbol_rep(i) for i in (x.left, x.right)))
    elif isinstance(x, lab.Num):
        return ('Num', x.n)
    elif isinstance(x, lab.Var):
        return ('Var', x.name)
    else:
        raise NotImplementedError('No support for %s' % x.__class__.__name__)


def symbol_hash(x):
    return hash(symbol_rep(x))


# read in expected result
def read_expected(fname):
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', fname), 'r') as f:
        return safe_eval(f.read())


def test_combinations_00():
    result = 0 + lab.Var('x')
    expected = ('Add', frozenset({('Var', 'x'), ('Num', 0)}))
    assert symbol_rep(result) == expected

    result = lab.Var('x') + 0
    expected = ('Add', frozenset({('Var', 'x'), ('Num', 0)}))
    assert symbol_rep(result) == expected

    result = 0 + (lab.Var('y') * 2)
    expected = ('Add', frozenset({('Mul', frozenset({('Num', 2), ('Var', 'y')})), ('Num', 0)}))
    assert symbol_rep(result) == expected

    result = ('z' * lab.Num(3)) + 0
    expected = ('Add', frozenset({('Mul', frozenset({('Num', 3), ('Var', 'z')})), ('Num', 0)}))
    assert symbol_rep(result) == expected

    result = (lab.Num(0) + 'x') * 'z'
    expected = ('Mul', frozenset({('Var', 'z'), ('Add', frozenset({('Var', 'x'), ('Num', 0)}))}))
    assert symbol_rep(result) == expected

    result = ((0 * lab.Var('y')) + lab.Var('x'))
    expected = ('Add', frozenset({('Mul', frozenset({('Var', 'y'), ('Num', 0)})), ('Var', 'x')}))
    assert symbol_rep(result) == expected

    result = ('x' + (lab.Num(2)-2))
    expected = ('Add', frozenset({('Var', 'x'), ('Sub', (('Num', 2), ('Num', 2)))}))
    assert symbol_rep(result) == expected

    result = 20 + lab.Num(101) * (1 * lab.Var('z'))
    expected = ('Add', frozenset({('Mul', frozenset({('Mul', frozenset({('Num', 1), ('Var', 'z')})), ('Num', 101)})), ('Num', 20)}))
    assert symbol_rep(result) == expected

    result = 'x' - lab.Num(101)
    expected = ('Sub', (('Var', 'x'), ('Num', 101)))
    assert symbol_rep(result) == expected

    result = 'x' / lab.Num(101)
    expected = ('Div', (('Var', 'x'), ('Num', 101)))
    assert symbol_rep(result) == expected

    result = lab.Num(101) / 'x'
    expected = ('Div', (('Num', 101), ('Var', 'x')))
    assert symbol_rep(result) == expected

    result = lab.Num(101) - 'x'
    expected = ('Sub', (('Num', 101), ('Var', 'x')))
    assert symbol_rep(result) == expected



def test_display_00():
    exp = lab.Add(lab.Num(0), lab.Var('x'))
    expected = ("Add(Num(0), Var('x'))", '0 + x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Var('x'), lab.Num(0))
    expected = ("Add(Var('x'), Num(0))", 'x + 0')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Num(1), lab.Var('x'))
    expected = ("Mul(Num(1), Var('x'))", '1 * x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Var('x'), lab.Num(1))
    expected = ("Mul(Var('x'), Num(1))", 'x * 1')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Var('x'), lab.Num(0))
    expected = ("Sub(Var('x'), Num(0))", 'x - 0')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Var('x'), lab.Num(1))
    expected = ("Div(Var('x'), Num(1))", 'x / 1')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Num(0), lab.Var('x'))
    expected = ("Div(Num(0), Var('x'))", '0 / x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Num(20), lab.Num(30))
    expected = ('Add(Num(20), Num(30))', '20 + 30')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Num(50), lab.Num(80))
    expected = ('Sub(Num(50), Num(80))', '50 - 80')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Num(40), lab.Num(20))
    expected = ('Div(Num(40), Num(20))', '40 / 20')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Num(101), lab.Num(121))
    expected = ('Mul(Num(101), Num(121))', '101 * 121')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]



def test_display_01():
    exp = lab.Add(lab.Num(0), lab.Mul(lab.Var('y'), lab.Num(2)))
    expected = ("Add(Num(0), Mul(Var('y'), Num(2)))", '0 + y * 2')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Mul(lab.Var('z'), lab.Num(3)), lab.Num(0))
    expected = ("Add(Mul(Var('z'), Num(3)), Num(0))", 'z * 3 + 0')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Num(1), lab.Add(lab.Var('A'), lab.Var('x')))
    expected = ("Mul(Num(1), Add(Var('A'), Var('x')))", '1 * (A + x)')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Sub(lab.Var('x'), lab.Var('A')), lab.Num(1))
    expected = ("Mul(Sub(Var('x'), Var('A')), Num(1))", '(x - A) * 1')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Mul(lab.Var('x'), lab.Num(3)), lab.Num(0))
    expected = ("Sub(Mul(Var('x'), Num(3)), Num(0))", 'x * 3 - 0')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Mul(lab.Num(7), lab.Var('A')), lab.Num(1))
    expected = ("Div(Mul(Num(7), Var('A')), Num(1))", '7 * A / 1')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Num(0), lab.Add(lab.Var('A'), lab.Num(3)))
    expected = ("Div(Num(0), Add(Var('A'), Num(3)))", '0 / (A + 3)')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Add(lab.Num(0), lab.Var('x')), lab.Var('z'))
    expected = ("Mul(Add(Num(0), Var('x')), Var('z'))", '(0 + x) * z')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Add(lab.Var('x'), lab.Num(0)), lab.Var('A'))
    expected = ("Sub(Add(Var('x'), Num(0)), Var('A'))", 'x + 0 - A')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Mul(lab.Num(1), lab.Var('x')), lab.Var('y'))
    expected = ("Add(Mul(Num(1), Var('x')), Var('y'))", '1 * x + y')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Var('z'), lab.Mul(lab.Var('x'), lab.Num(1)))
    expected = ("Add(Var('z'), Mul(Var('x'), Num(1)))", 'z + x * 1')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Var('A'), lab.Sub(lab.Var('x'), lab.Num(0)))
    expected = ("Sub(Var('A'), Sub(Var('x'), Num(0)))", 'A - (x - 0)')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Var('y'), lab.Div(lab.Var('x'), lab.Num(1)))
    expected = ("Div(Var('y'), Div(Var('x'), Num(1)))", 'y / (x / 1)')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Var('z'), lab.Div(lab.Num(0), lab.Var('x')))
    expected = ("Mul(Var('z'), Div(Num(0), Var('x')))", 'z * 0 / x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Mul(lab.Num(0), lab.Var('y')), lab.Var('x'))
    expected = ("Add(Mul(Num(0), Var('y')), Var('x'))", '0 * y + x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Var('x'), lab.Sub(lab.Num(2), lab.Num(2)))
    expected = ("Add(Var('x'), Sub(Num(2), Num(2)))", 'x + 2 - 2')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Div(lab.Num(2), lab.Num(2)), lab.Var('x'))
    expected = ("Mul(Div(Num(2), Num(2)), Var('x'))", '2 / 2 * x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Var('x'), lab.Sub(lab.Num(3), lab.Num(2)))
    expected = ("Mul(Var('x'), Sub(Num(3), Num(2)))", 'x * (3 - 2)')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Var('x'), lab.Mul(lab.Num(0), lab.Var('z')))
    expected = ("Sub(Var('x'), Mul(Num(0), Var('z')))", 'x - 0 * z')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Var('x'), lab.Num(1))
    expected = ("Div(Var('x'), Num(1))", 'x / 1')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Div(lab.Add(lab.Num(0), lab.Num(0)), lab.Var('x'))
    expected = ("Div(Add(Num(0), Num(0)), Var('x'))", '(0 + 0) / x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('52_in.pyobj')
    expected = read_expected('52_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Add(lab.Num(70), lab.Num(50)), lab.Num(80))
    expected = ('Sub(Add(Num(70), Num(50)), Num(80))', '70 + 50 - 80')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Sub(lab.Num(80), lab.Div(lab.Num(40), lab.Num(20)))
    expected = ('Sub(Num(80), Div(Num(40), Num(20)))', '80 - 40 / 20')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('55_in.pyobj')
    expected = read_expected('55_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]



def test_display_02():
    exp = read_expected('56_in.pyobj')
    expected = read_expected('56_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('57_in.pyobj')
    expected = read_expected('57_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('58_in.pyobj')
    expected = read_expected('58_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('59_in.pyobj')
    expected = read_expected('59_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('60_in.pyobj')
    expected = read_expected('60_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('61_in.pyobj')
    expected = read_expected('61_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('62_in.pyobj')
    expected = read_expected('62_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('63_in.pyobj')
    expected = read_expected('63_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]


def test_deriv_00():
    exp = lab.Add(lab.Var('x'), lab.Mul(lab.Var('x'), lab.Var('x')))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('74_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = read_expected('75_in.pyobj')
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('75_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = read_expected('76_in.pyobj')
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('76_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Mul(lab.Mul(lab.Var('x'), lab.Var('x')), lab.Var('x'))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('77_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Mul(lab.Mul(lab.Var('x'), lab.Var('y')), lab.Var('z'))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('78_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = read_expected('79_in.pyobj')
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('79_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Add(lab.Add(lab.Num(0), lab.Var('y')), lab.Var('x'))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('80_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Num(0)
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = [lab.Num(0), lab.Num(0), lab.Num(0), lab.Num(0), lab.Num(0)]
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Sub(lab.Var('x'), lab.Mul(lab.Var('x'), lab.Var('x')))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('82_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Sub(lab.Mul(lab.Var('x'), lab.Var('x')), lab.Var('x'))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('83_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Div(lab.Var('y'), lab.Mul(lab.Var('x'), lab.Var('x')))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('84_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Div(lab.Mul(lab.Var('x'), lab.Var('x')), lab.Var('y'))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('85_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = read_expected('86_in.pyobj')
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('x').deriv('x').deriv('x'), exp.deriv('y').deriv('x'), exp.deriv('z'))
    expected = read_expected('86_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)


def test_simplify_00():
    result = lab.Add(lab.Num(0), lab.Var('x')).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Var('x'), lab.Num(0)).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Num(1), lab.Var('x')).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Var('x'), lab.Num(1)).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Var('x'), lab.Num(0)).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Var('x'), lab.Num(1)).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Num(0), lab.Var('x')).simplify()
    expected = lab.Num(0)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Num(20), lab.Num(30)).simplify()
    expected = lab.Num(50)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Num(50), lab.Num(80)).simplify()
    expected = lab.Num(-30)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Num(40), lab.Num(20)).simplify()
    expected = lab.Num(2.0)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Num(101), lab.Num(121)).simplify()
    expected = lab.Num(12221)
    assert symbol_rep(result) == symbol_rep(expected)



def test_simplify_01():
    result = lab.Add(lab.Num(0), lab.Mul(lab.Var('y'), lab.Num(2))).simplify()
    expected = lab.Mul(lab.Var('y'), lab.Num(2))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Mul(lab.Var('z'), lab.Num(3)), lab.Num(0)).simplify()
    expected = lab.Mul(lab.Var('z'), lab.Num(3))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Num(1), lab.Add(lab.Var('A'), lab.Var('x'))).simplify()
    expected = lab.Add(lab.Var('A'), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Sub(lab.Var('x'), lab.Var('A')), lab.Num(1)).simplify()
    expected = lab.Sub(lab.Var('x'), lab.Var('A'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Mul(lab.Var('x'), lab.Num(3)), lab.Num(0)).simplify()
    expected = lab.Mul(lab.Var('x'), lab.Num(3))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Mul(lab.Num(7), lab.Var('A')), lab.Num(1)).simplify()
    expected = lab.Mul(lab.Num(7), lab.Var('A'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Num(0), lab.Add(lab.Var('A'), lab.Num(3))).simplify()
    expected = lab.Num(0)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Add(lab.Num(0), lab.Var('x')), lab.Var('z')).simplify()
    expected = lab.Mul(lab.Var('x'), lab.Var('z'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Add(lab.Var('x'), lab.Num(0)), lab.Var('A')).simplify()
    expected = lab.Sub(lab.Var('x'), lab.Var('A'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Mul(lab.Num(1), lab.Var('x')), lab.Var('y')).simplify()
    expected = lab.Add(lab.Var('x'), lab.Var('y'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Var('z'), lab.Mul(lab.Var('x'), lab.Num(1))).simplify()
    expected = lab.Add(lab.Var('z'), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Var('A'), lab.Sub(lab.Var('x'), lab.Num(0))).simplify()
    expected = lab.Sub(lab.Var('A'), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Var('y'), lab.Div(lab.Var('x'), lab.Num(1))).simplify()
    expected = lab.Div(lab.Var('y'), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Var('z'), lab.Div(lab.Num(0), lab.Var('x'))).simplify()
    expected = lab.Num(0)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Mul(lab.Num(0), lab.Var('y')), lab.Var('x')).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Var('x'), lab.Sub(lab.Num(2), lab.Num(2))).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Div(lab.Num(2), lab.Num(2)), lab.Var('x')).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Mul(lab.Var('x'), lab.Sub(lab.Num(3), lab.Num(2))).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Var('x'), lab.Mul(lab.Num(0), lab.Var('z'))).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Var('x'), lab.Num(1)).simplify()
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Add(lab.Num(0), lab.Num(0)), lab.Var('x')).simplify()
    expected = lab.Num(0)
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('123_in.pyobj').simplify()
    expected = lab.Num(800)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Add(lab.Num(70), lab.Num(50)), lab.Num(80)).simplify()
    expected = lab.Num(40)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Sub(lab.Num(80), lab.Div(lab.Num(40), lab.Num(20))).simplify()
    expected = lab.Num(78.0)
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('126_in.pyobj').simplify()
    expected = lab.Add(lab.Num(20), lab.Mul(lab.Num(101), lab.Var('z')))
    assert symbol_rep(result) == symbol_rep(expected)



def test_simplify_02():
    result = lab.Sub(lab.Num(1), lab.Var('L')).simplify()
    expected = lab.Sub(lab.Num(1), lab.Var('L'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Add(lab.Var('b'), lab.Num(1)).simplify()
    expected = lab.Add(lab.Var('b'), lab.Num(1))
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('129_in.pyobj').simplify()
    expected = read_expected('129_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('130_in.pyobj').simplify()
    expected = read_expected('130_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('131_in.pyobj').simplify()
    expected = lab.Sub(lab.Div(lab.Num(-1), lab.Var('I')), lab.Num(-1))
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('132_in.pyobj').simplify()
    expected = read_expected('132_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Var('M'), lab.Var('D')).simplify()
    expected = lab.Div(lab.Var('M'), lab.Var('D'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('134_in.pyobj').simplify()
    expected = read_expected('134_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('135_in.pyobj').simplify()
    expected = read_expected('135_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('136_in.pyobj').simplify()
    expected = read_expected('136_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('137_in.pyobj').simplify()
    expected = read_expected('137_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Div(lab.Add(lab.Num(1), lab.Var('Q')), lab.Var('k')).simplify()
    expected = lab.Div(lab.Add(lab.Num(1), lab.Var('Q')), lab.Var('k'))
    assert symbol_rep(result) == symbol_rep(expected)


def test_eval_00():
    result = lab.Add(lab.Num(0), lab.Var('x'))
    result = result.eval({'x': 877})
    expected = 877
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Mul(lab.Num(1), lab.Var('x'))
    result = result.eval({'x': -365})
    expected = -365
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Mul(lab.Var('y'), lab.Num(2))
    result = result.eval({'y': -296})
    expected = -592
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Add(lab.Mul(lab.Var('z'), lab.Num(3)), lab.Num(0))
    result = result.eval({'z': 400})
    expected = 1200
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Div(lab.Mul(lab.Num(7), lab.Var('A')), lab.Num(9))
    result = result.eval({'A': 610})
    expected = 474.44444444444446
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Add(lab.Var('z'), lab.Add(lab.Var('x'), lab.Num(1)))
    result = result.eval({'z': -596, 'x': -554})
    expected = -1149
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Sub(lab.Var('A'), lab.Add(lab.Var('x'), lab.Var('A')))
    result = result.eval({'A': 539, 'x': -789})
    expected = 789
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Div(lab.Var('y'), lab.Div(lab.Var('x'), lab.Var('z')))
    result = result.eval({'z': 693, 'y': -71, 'x': -391})
    expected = 125.83887468030692
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Mul(lab.Mul(lab.Var('x'), lab.Var('y')), lab.Var('z'))
    result = result.eval({'z': 816, 'y': 732, 'x': -225})
    expected = -134395200
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('156_in.pyobj')
    result = result.eval({'z': 984, 'A': -801, 'x': -880, 'y': 96})
    expected = -1815480
    assert abs(result/expected - 1) <= 1e-4



def test_eval_01():
    result = lab.Sub(lab.Var('k'), lab.Num(5))
    result = result.eval({'k': 583})
    expected = 578
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('158_in.pyobj')
    result = result.eval({'Q': -960, 'T': 696, 'Y': 895, 'H': -395, 'y': -752, 'F': 973, 'l': 581, 'X': 853, 'G': -370, 'q': -403, 'V': 211, 'v': 203, 'n': -859, 't': -794, 'o': -710, 'N': 640, 'L': 958, 'g': 46, 'J': 796, 'f': 127, 'w': 706, 'S': 351, 'B': 454, 'O': 45, 'D': 848, 'u': -729, 'E': 394, 'C': -230, 'p': -497, 'a': 494, 'Z': 890, 'j': 601, 'K': -273, 'I': -432, 'e': 809, 's': 453, 'i': -90, 'R': 421, 'U': 720, 'P': -248, 'm': 56, 'k': -20})
    expected = -24447405.102586962
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('159_in.pyobj')
    result = result.eval({'P': 865, 'r': -635, 'g': -328, 'L': -77, 'b': 272, 'B': -892, 'h': 569, 'H': -411, 'D': 606, 'y': -891, 'W': 278, 'u': 411, 'p': 769, 'C': -557, 'z': -478, 'j': 547, 'A': -273, 'K': -671, 'I': 156, 'M': -942, 's': -991, 'V': 33, 'U': 951, 'm': 695, 't': 337, 'o': -27, 'N': -392, 'k': 865})
    expected = 3.079655919243488e-13
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('160_in.pyobj')
    result = result.eval({'r': -831, 'Q': -249, 'T': -12, 'H': -582, 'l': -408, 'G': -796, 'V': -412, 'n': -166, 'N': -116, 'g': 30, 'S': -281, 'B': 969, 'x': -690, 'O': 17, 'W': -977, 'u': 844, 'C': -425, 'Z': -304, 'j': -617, 'A': 757, 'I': 742, 'i': -660, 'U': -916, 'R': -46, 'b': -809, 'y': -861, 'F': 316, 'z': 295, 'q': 201, 'M': 368, 'v': 952, 't': -597, 'd': 874, 'o': 745, 'L': 812, 'J': -55, 'w': 153, 'h': -249, 'D': -310, 'p': 289, 's': -535, 'P': 629, 'm': 705, 'k': -130})
    expected = -3036189255.554901
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('161_in.pyobj')
    result = result.eval({'g': 867, 'L': 954, 'w': 686, 'f': -711, 'o': -227, 'h': -634, 'O': 799, 'y': 594, 'D': -115, 'u': 394, 'a': 960, 'X': -987, 'v': -163, 'U': -887, 't': 527, 'd': 657, 'N': 400})
    expected = 4741737.246211018
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('162_in.pyobj')
    result = result.eval({'J': -150, 'X': -302, 'w': 332, 's': 927, 'v': -687, 'B': -740, 'E': 671, 'k': -539})
    expected = 347.0000000000164
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('163_in.pyobj')
    result = result.eval({'P': -228, 'Q': -6, 'g': 896, 'd': -417, 'T': -870, 'b': -138, 'S': 835, 'x': -405, 'h': 719, 'H': 766, 'y': -982, 'D': 766, 'E': -376, 'C': 832, 'l': -559, 'X': 323, 'K': -630, 'q': 548, 'I': -809, 'V': -849, 'M': 122, 'c': 173, 'o': -875, 'm': -395})
    expected = -4004783415.5644646
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('164_in.pyobj')
    result = result.eval({'L': -750, 'd': -449, 'T': -230, 'f': -843, 'o': 280, 'O': -840, 'h': -729, 'y': -658, 'D': -724, 'W': 502, 'E': 578, 'F': -198, 'Z': -23, 'e': 360, 'v': 666, 'U': 927, 'm': 230, 't': -944, 'P': 742, 'N': 446})
    expected = 1475.6592465238434
    assert abs(result/expected - 1) <= 1e-4


def test_parse_00():
    result = lab.expression('x')
    expected = lab.Var('x')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('20')
    expected = lab.Num(20)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(0 + x)')
    expected = lab.Add(lab.Num(0), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(-101 * x)')
    expected = lab.Mul(lab.Num(-101), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(y * -2)')
    expected = lab.Mul(lab.Var('y'), lab.Num(-2))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((z * 3) + 0)')
    expected = lab.Add(lab.Mul(lab.Var('z'), lab.Num(3)), lab.Num(0))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((7 * A) / 9)')
    expected = lab.Div(lab.Mul(lab.Num(7), lab.Var('A')), lab.Num(9))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(z + (x + 1))')
    expected = lab.Add(lab.Var('z'), lab.Add(lab.Var('x'), lab.Num(1)))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(A - (x + A))')
    expected = lab.Sub(lab.Var('A'), lab.Add(lab.Var('x'), lab.Var('A')))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(y / (x / z))')
    expected = lab.Div(lab.Var('y'), lab.Div(lab.Var('x'), lab.Var('z')))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((x * y) * z)')
    expected = lab.Mul(lab.Mul(lab.Var('x'), lab.Var('y')), lab.Var('z'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((x + A) * (y + z))')
    expected = read_expected('187_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)



def test_parse_01():
    result = lab.expression(read_expected('188_in.pyobj'))
    expected = read_expected('188_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('189_in.pyobj'))
    expected = read_expected('189_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('190_in.pyobj'))
    expected = read_expected('190_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('191_in.pyobj'))
    expected = read_expected('191_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)


def test_pow():
    result = 0 ** lab.Var('x')
    expected = ('Pow', (('Num', 0), ('Var', 'x')))
    assert symbol_rep(result) == expected

    result = lab.Var('x') ** 0
    expected = ('Pow', (('Var', 'x'), ('Num', 0)))
    assert symbol_rep(result) == expected

    result = 3 ** (lab.Var('y') ** 2)
    expected = ('Pow', (('Num', 3), ('Pow', (('Var', 'y'), ('Num', 2)))))
    assert symbol_rep(result) == expected

    result = ((0 * lab.Var('y')) ** lab.Var('x'))
    expected = ('Pow', (('Mul', frozenset({('Var', 'y'), ('Num', 0)})), ('Var', 'x')))
    assert symbol_rep(result) == expected

    result = ('x' + (lab.Num(2)**2))
    expected = ('Add', frozenset({('Pow', (('Num', 2), ('Num', 2))), ('Var', 'x')}))
    assert symbol_rep(result) == expected

    result = 20 + lab.Num(101) * (1 * lab.Var('z'))
    expected = ('Add', frozenset({('Mul', frozenset({('Mul', frozenset({('Num', 1), ('Var', 'z')})), ('Num', 101)})), ('Num', 20)}))
    assert symbol_rep(result) == expected

    result = 'x' ** lab.Num(101)
    expected = ('Pow', (('Var', 'x'), ('Num', 101)))
    assert symbol_rep(result) == expected

    exp = lab.Add(lab.Pow(lab.Num(0), lab.Var('y')), lab.Var('x'))
    expected = ("Add(Pow(Num(0), Var('y')), Var('x'))", '0 ** y + x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Add(lab.Var('x'), lab.Pow(lab.Num(2), lab.Num(2)))
    expected = ("Add(Var('x'), Pow(Num(2), Num(2)))", 'x + 2 ** 2')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Div(lab.Num(2), lab.Num(2)), lab.Var('x'))
    expected = ("Mul(Div(Num(2), Num(2)), Var('x'))", '2 / 2 * x')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Mul(lab.Var('x'), lab.Sub(lab.Num(3), lab.Num(2)))
    expected = ("Mul(Var('x'), Sub(Num(3), Num(2)))", 'x * (3 - 2)')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Pow(lab.Var('x'), lab.Pow(lab.Num(2), lab.Var('z')))
    expected = ("Pow(Var('x'), Pow(Num(2), Var('z')))", 'x ** 2 ** z')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Pow(lab.Pow(lab.Var('x'), lab.Num(2)), lab.Var('z'))
    expected = ("Pow(Pow(Var('x'), Num(2)), Var('z'))", '(x ** 2) ** z')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Pow(lab.Var('x'), lab.Num(1))
    expected = ("Pow(Var('x'), Num(1))", 'x ** 1')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('71_in.pyobj')
    expected = read_expected('71_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('72_in.pyobj')
    expected = read_expected('72_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = read_expected('73_in.pyobj')
    expected = read_expected('73_out.pyobj')
    assert symbol_rep(safe_eval(repr(exp))) == symbol_rep(safe_eval(expected[0]))
    assert str(exp) == expected[1]

    exp = lab.Pow(lab.Var('x'), lab.Num(2))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('z'), exp.deriv('b'))
    expected = read_expected('87_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Pow(lab.Var('x'), lab.Num(1))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('z'), exp.deriv('b'))
    expected = read_expected('88_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = lab.Pow(lab.Add(lab.Var('x'), lab.Var('y')), lab.Num(4))
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('z'), exp.deriv('b'))
    expected = read_expected('89_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    exp = read_expected('90_in.pyobj')
    out = (exp.deriv('x'), exp.deriv('y'), exp.deriv('z'), exp.deriv('b'))
    expected = read_expected('90_out.pyobj')
    for i, j in zip(out, expected):
        assert symbol_rep(i) == symbol_rep(j)

    result = read_expected('139_in.pyobj').simplify()
    expected = lab.Num(1)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Pow(lab.Var('x'), lab.Num(0)).simplify()
    expected = lab.Num(1)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Pow(lab.Num(0), lab.Var('x')).simplify()
    expected = lab.Num(0)
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Pow(lab.Var('x'), lab.Pow(lab.Var('y'), lab.Var('z'))).simplify()
    expected = lab.Pow(lab.Var('x'), lab.Pow(lab.Var('y'), lab.Var('z')))
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('143_in.pyobj').simplify()
    expected = lab.Add(lab.Num(3), lab.Mul(lab.Var('x'), lab.Var('z')))
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('144_in.pyobj').simplify()
    expected = lab.Mul(lab.Num(2), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('145_in.pyobj').simplify()
    expected = read_expected('145_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = read_expected('146_in.pyobj').simplify()
    expected = read_expected('146_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.Pow(lab.Var('x'), lab.Num(2))
    result = result.eval({'x': 237})
    expected = 56169
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Pow(lab.Mul(lab.Var('x'), lab.Var('y')), lab.Var('z'))
    result = result.eval({'z': 758, 'y': 95, 'x': -530})
    expected = read_expected('166_out.pyobj')
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Pow(lab.Pow(lab.Var('x'), lab.Num(2)), lab.Num(0))
    result = result.eval({'x': 80})
    expected = 1
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Pow(lab.Sub(lab.Num(5), lab.Num(3)), lab.Var('x'))
    result = result.eval({'x': 960})
    expected = read_expected('168_out.pyobj')
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('169_in.pyobj')
    result = result.eval({'L': -955, 'd': -476, 'T': 127, 'f': 569, 'O': 763, 'H': -196, 'y': 655, 'D': 290, 'E': -384, 'p': -250, 'z': 20, 'Z': -16, 'X': -737, 'A': -541, 'K': -61, 'q': 404, 'I': -740, 's': -505, 'e': 510, 'v': 195, 'R': 320, 'U': 694, 't': 893, 'o': 223, 'N': 578})
    expected = 69606.30569229023
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('170_in.pyobj')
    result = result.eval({'Q': 270, 'L': -362, 'T': -931, 'S': -184, 'B': 121, 'O': -946, 'H': -529, 'W': 915, 'E': -41, 'C': 377, 'F': 494, 'z': 918, 'X': -767, 's': 781, 'M': -710, 'i': -916, 'U': 480, 't': -500, 'P': 831, 'm': -908})
    expected = -0.0031834854228580413
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('171_in.pyobj')
    result = result.eval({'r': -847, 'Q': 383, 'L': 726, 'g': 659, 'b': 126, 'T': 458, 'f': -395, 'w': 993, 'x': 243, 'h': -472, 'D': 504, 'W': 416, 'l': -256, 'G': -93, 'I': -54, 'v': 579, 'i': -85, 'U': 565, 'P': -247, 'm': 8})
    expected = (0.99156973760839-0.004704475218913467j)
    assert abs(result/expected - 1) <= 1e-4

    result = lab.Sub(lab.Num(5), lab.Num(-4))
    result = result.eval({})
    expected = 9
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('173_in.pyobj')
    result = result.eval({'r': -233, 'Q': 195, 'g': -231, 'J': -161, 'L': 644, 'b': -309, 'T': 111, 'S': -568, 'B': -793, 'h': 179, 'H': 780, 'y': 358, 'D': -587, 'W': -781, 'u': -285, 'p': 586, 'C': 83, 'F': 657, 'z': 562, 'Z': -868, 'j': -351, 'G': -498, 'K': 207, 'q': -818, 'I': 233, 'V': 738, 'M': -726, 's': -365, 'i': -352, 'U': 272, 'k': -193})
    expected = -656389.8154121593
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('174_in.pyobj')
    result = result.eval({'r': -234, 'Q': -923, 'd': 686, 'f': 858, 'o': 865, 'O': -380, 'h': 730, 'W': -277, 'u': 566, 'C': 510, 'l': -458, 'X': 262, 'G': 831, 'K': 652, 'I': 212, 's': -621, 'M': -54, 'e': 733, 'i': 241, 'U': -938, 'N': 237, 'c': 445, 'P': -134, 'm': -529, 'k': -852})
    expected = 916.25
    assert abs(result/expected - 1) <= 1e-4

    result = read_expected('175_in.pyobj')
    result = result.eval({'b': -966, 'T': 598, 'f': -148, 'w': 154, 'S': 420, 'B': 673, 'x': 597, 'y': 719, 'E': -196, 'p': 314, 'u': -673, 'F': 758, 'C': -956, 'a': 709, 'l': 174, 'A': 893, 'G': -837, 'K': -916, 'q': 979, 'I': 788, 'M': -797, 'e': -613, 'v': 764, 'i': -581, 'U': 950, 'c': 869, 'P': 521, 'N': 837, 'k': 560})
    expected = 855.4328021463105
    assert abs(result/expected - 1) <= 1e-4

    result = lab.expression('(3 ** x)')
    expected = lab.Pow(lab.Num(3), lab.Var('x'))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(y ** -2)')
    expected = lab.Pow(lab.Var('y'), lab.Num(-2))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((z ** 3) + 0)')
    expected = lab.Add(lab.Pow(lab.Var('z'), lab.Num(3)), lab.Num(0))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((7 ** A) / 9)')
    expected = lab.Div(lab.Pow(lab.Num(7), lab.Var('A')), lab.Num(9))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(z ** (x + 1))')
    expected = lab.Pow(lab.Var('z'), lab.Add(lab.Var('x'), lab.Num(1)))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((z ** x) ** 1)')
    expected = lab.Pow(lab.Pow(lab.Var('z'), lab.Var('x')), lab.Num(1))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(A - (x ** A))')
    expected = lab.Sub(lab.Var('A'), lab.Pow(lab.Var('x'), lab.Var('A')))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('(y ** (x / z))')
    expected = lab.Pow(lab.Var('y'), lab.Div(lab.Var('x'), lab.Var('z')))
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression('((x + A) ** (y + z))')
    expected = read_expected('200_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('201_in.pyobj'))
    expected = read_expected('201_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('202_in.pyobj'))
    expected = read_expected('202_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('203_in.pyobj'))
    expected = read_expected('203_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('204_in.pyobj'))
    expected = read_expected('204_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('205_in.pyobj'))
    expected = read_expected('205_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)

    result = lab.expression(read_expected('206_in.pyobj'))
    expected = read_expected('206_out.pyobj')
    assert symbol_rep(result) == symbol_rep(expected)


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
