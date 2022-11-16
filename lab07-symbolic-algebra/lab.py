import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

def isAZaz(c):
    return (65 <= ord(c) <= 90 or # Upper Case
        97 <= ord(c) <= 122) # Lower Case

def tokenize(expression):
    """
    Assume <expression> ::= (E1 op E2), 
    where E1, E2 are numbers, variables, or expressions themselves.

    Return a ordered list of tokens that make up the expression
    """
    if expression[0] != '(':
        return [expression]

    chararr =[c for c in expression if not c.isspace()]
    ttemp = []
    tl = []

    l = len(chararr)
    i = 0
    while i < l: 
        c = chararr[i]
        if c == '*' and chararr[i + 1] == '*':
            tl.append('**')
            i += 2
            continue

        elif (isAZaz(c) or
            c in ['+', '*', '/', '(', ')'] or
            i > 0 and chararr[i - 1] not in ['+', '-', '*', '/', '('] and c == '-' # '-' is interpreted as a minus sign only if it succeeds a number or a ')'
            ):
            tl.append(c)

        else:
            ttemp.append(c)
            if i + 1 < len(chararr) and not chararr[i + 1].isdigit():
                tl.append(''.join(ttemp))
                ttemp = []

        i += 1

    return tl

def parse(tl):
    def parse_expression(i):
        if tl[i].isdigit() or len(tl[i]) > 1:
            return Num(int(tl[i])), i + 1
        elif 'a' <= tl[i] <= 'z' or 'A' <= tl[i] <='Z':
            return Var(tl[i]), i + 1
        else: # '(' or 'BinOp' or ')'
            if tl[i] == '(':
                e1, ni = parse_expression(i + 1)

            while tl[ni] != ')':
                # print(e1)
                op = sym_to_constructor(tl[ni])
                e2, ni = parse_expression(ni + 1)
                e1 = op(e1, e2)
                # print(e1)

            return e1, ni + 1

    parse_expression, next_index = parse_expression(0)
    return parse_expression

def expression(human_input):
    tl = tokenize(human_input)
    print(tl)
    return parse(tl)

def sym_to_constructor(sym):
    sym_to_cons = {
        '+': Add,
        '-': Sub,
        '*': Mul,
        '/': Div,
        '**': Pow,
    }
    # assert sym in sym_to_cons
    return sym_to_cons[sym]

class Symbol:
    def __init__(self, name=""):
        self.name = name

    def __add__(self, other):
        return Add(self, other)
            
    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)            
            
    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        return Div(other, self)

    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return Pow(other, self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Symbol({self.name})'


class BinOp(Symbol):
    def __init__(self, name, loperand, roperand):
        Symbol.__init__(self, name)
        if isinstance(loperand, int) or \
        isinstance(loperand, str) and loperand.isdigit():
            self.left = Num(loperand)
        elif isinstance(loperand, str):
            self.left = Var(loperand)
        else:
            self.left = loperand

        if isinstance(roperand, int) or \
        isinstance(roperand, str) and roperand.isdigit():
            self.right = Num(roperand)
        elif isinstance(roperand, str):
            self.right = Var(roperand)
        else:
            self.right = roperand

    def __str__(self):
        # Precedence
        # mul/div > add/sub   

        left = self.left
        right = self.right
        if self.name == 'Pow':
            # print("called")
            if self.precedence >= self.left.precedence:
                left = f'({str(self.left)})'
        else:
            if self.precedence > self.left.precedence:
                left = f'({str(self.left)})'

        if (self.precedence > self.right.precedence or
           self.sym in ['-', '/'] and self.precedence == self.right.precedence): # example for second condition: x / y * z !=  x / (y * z) 
            right = f'({str(self.right)})'

        return f'{left} {self.sym} {right}'


    def __repr__(self):
        return f'{str(self.name)}({repr(self.left)}, {repr(self.right)})'

    # Internal function used by simplify()
    def simplifyTwoNumbers(self):
        l, r = self.left, self.right
        # Binary operation on two numbers simplifies to a single number containing the result.
        if self.sym == '+':
            return Num(l.n + r.n)
        elif self.sym == '-':
            return Num(l.n - r.n)
        elif self.sym == '*':
            return Num(l.n * r.n)
        elif self.sym == '/':
            return Num(l.n / r.n)
            
        # else: 
        #     if self.sym == '+':
        #         return l.simplify() + r.simplify()
        #     elif self.sym == '-':
        #         return l.simplify() - r.simplify()
        #     elif self.sym == '*':
        #         return l.simplify() * r.simplify()
        #     elif self.sym == '/':
        #         return l.simplify() / r.simplify()

        # elif isinstance(l, Num) and l.n == 0:
        #     # Additive identity (LHS)
        #     if self.sym == '+': # e.g. 0 + E = E
        #         return r
        #     # Multiplicative/Divisive anniliation
        #     elif self.sym in ['*', '/']: 
        #         # e.g. 0 * E = 0, and 0 / E = 0
        #         return Num(0)

        # elif isinstance(r, Num) and r.n == 1: 
        #     # Multiplicative/Divisive identity (RHS)
        #     if self.sym in ['*', '/']: 
        #         # e.g. E * 1 = E, and E / 1 = E 
        #         return l 

    def eval(self, mapping):
        lv = self.left.eval(mapping)
        rv = self.right.eval(mapping)

        assert isinstance(lv, (int, float)), f'lv type: {type(lv)} is not a number!!'
        assert isinstance(rv, (int, float)), f'rv type: {type(rv)} is not a number!!'

        # Binary operation on two numbers simplifies to a single number containing the result.
        if self.sym == '+':
            return lv + rv
        elif self.sym == '-':
            return lv - rv
        elif self.sym == '*':
            return lv * rv
        elif self.sym == '/':
            return lv / rv
        elif self.sym == '**':
            return lv ** rv


class Add(BinOp):
    precedence = 1
    sym = '+'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Add', loperand, roperand)

    # def __str__(self):
    #     # no type checking
    #     if isinstance(self.left, Var) and isinstance(self.right, Var): 
    #         return f'{self.left} + {self.right}'

    def deriv(self, x):
        return self.left.deriv(x) + self.right.deriv(x)

    def simplify(self): 
        l, r = self.left, self.right
        # if left or right is binop 
        # divide and conquer

        # divide and conquer
        ls = l.simplify()
        rs = r.simplify()

        # merge
        if isinstance(ls, Num) and isinstance(rs, Num):
            return Num(ls.n + rs.n)
        elif isinstance(rs, Num) and rs.n == 0: # Additive identity (RHS)
            return ls
        elif isinstance(ls, Num) and ls.n == 0: # Additive identity (LHS)
            return rs
        else:
            return Add(ls, rs)


class Sub(BinOp):
    precedence = 1
    sym = '-'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Sub', loperand, roperand)


    def deriv(self, x):
        return self.left.deriv(x) - self.right.deriv(x)

    def simplify(self): 
        l, r = self.left, self.right

        # divide and conquer
        ls = l.simplify()
        rs = r.simplify()

        if isinstance(ls, Num) and isinstance(rs, Num):
            return Num(ls.n - rs.n)
        elif isinstance(rs, Num) and rs.n == 0: # Subtractive identity (RHS)
            return ls
        else: 
            return ls - rs


class Mul(BinOp):
    precedence = 2
    sym = '*'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Mul', loperand, roperand)

    def deriv(self, x):
        return self.left * self.right.deriv(x) + self.right * self.left.deriv(x)

    def simplify(self): 
        l, r = self.left, self.right

        # divide and conquer
        ls = l.simplify()
        rs = r.simplify()

        # Multiplicative anniliation
        if isinstance(ls, Num) and isinstance(rs, Num):
            return Num(ls.n * rs.n)
        elif isinstance(rs, Num) and rs.n == 0 or \
           isinstance(ls, Num) and ls.n == 0: 
            return Num(0)

        # Multiplicative identity
        elif isinstance(rs, Num) and rs.n == 1:
            return ls
        elif isinstance(ls, Num) and ls.n == 1:
            return rs
        else:
            return ls * rs


class Div(BinOp):
    precedence = 2
    sym = '/'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Div', loperand, roperand)

    def deriv(self, x):
        u, v = self.left, self.right
        return (v * u.deriv(x) - u * v.deriv(x)) / (v * v)

    def simplify(self): 
        l, r = self.left, self.right

        # divide and conquer
        ls = l.simplify()
        rs = r.simplify()
        if isinstance(ls, Num) and isinstance(rs, Num):
            return Num(ls.n / rs.n)
        elif isinstance(rs, Num) and rs.n == 1:
            return ls
        elif isinstance(ls, Num) and ls.n == 0:
            return Num(0)
        else:
            return ls / rs


class Pow(BinOp):
    precedence = 3
    sym = '**'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Pow', loperand, roperand)

    def deriv(self, x):
        u, n = self.left, self.right

        _ = n.eval({})
        if type(_) == int:
            _ = Num(_)

        if type(_) == Num:
            return _ * u ** (_ - 1) * u.deriv(x) 
                
        # print(type(_))

        raise TypeError("Unsupported type for Pow(x, n). n should only be an instance of num.")

    def simplify(self):
        l, r = self.left, self.right

        # divide and conquer
        ls = l.simplify()
        rs = r.simplify()

        # merge
        if isinstance(ls, Num) and isinstance(rs, Num):
            return Num(ls.n ** rs.n)
        elif isinstance(rs, Num) and rs.n == 0:
            return Num(1)
        elif isinstance(rs, Num) and rs.n == 1:
            return ls
        elif isinstance(ls, Num) and ls.n == 0:
            return Num(0)
        else:
            return ls ** rs


class Var(Symbol):
    precedence = float('inf')
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Var("{str(self.name)}")'

    def deriv(self, x):
        assert isinstance(x, str)
        if x == self.name:
            return Num(1)
        else:
            return Num(0)

    def simplify(self):
        return self

    def eval(self, mapping):
        if self.name in mapping:
            return mapping[self.name]
        else: 
            # This var can't not be evaluated for a lack of mapping
            return self


class Num(Symbol):
    precedence = float('inf')
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        if isinstance(n, str):
            if n.isdigit():
                self.n = int(n)
            else:
                self.n = float(n)

        elif type(n) == int or type(n) == float:
            self.n = n

        else:
            raise ValueError("<Num> cannot parse non-numeric type!!")

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f'Num({str(self.n)})'

    def deriv(self, x):
        return Num(0)

    def simplify(self):
        return self

    def eval(self, mapping):
        return self.n


if __name__ == "__main__":
    doctest.testmod()
