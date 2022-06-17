import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


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
        # Only implement integer exponents for now
        assert isinstance(other, int), "Non-integer exponent is not supported!!"
        if other == 0:
            return Num(1)
        res = self
        for _ in range(other - 1):
            res *= self
        return res 


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
        if self.precedence > self.left.precedence:
            left = f'({str(self.left)})'

        if (self.precedence > self.right.precedence or
           self.sym in ['-', '/'] and self.precedence == self.right.precedence): # example for second condition: x / y * z !=  x / (y * z) 
            right = f'({str(self.right)})'


        return f'{left} {self.sym} {right}'


    def __repr__(self):
        return f'{str(self.name)}({repr(self.left)}, {repr(self.right)})'


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

class Sub(BinOp):
    precedence = 1
    sym = '-'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Sub', loperand, roperand)


    def deriv(self, x):
        return self.left.deriv(x) - self.right.deriv(x)


class Mul(BinOp):
    precedence = 2
    sym = '*'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Mul', loperand, roperand)

    def deriv(self, x):
        return self.left * self.right.deriv(x) + self.right * self.left.deriv(x)


class Div(BinOp):
    precedence = 2
    sym = '/'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Div', loperand, roperand)

    def deriv(self, x):
        assert isinstance(x, str)
        u, v = self.left, self.right
        return (v * u.deriv(x) - u * v.deriv(x)) / (v ** 2)


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


class Num(Symbol):
    precedence = float('inf')
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f'Num({str(self.n)})'

    def deriv(self, x):
        return Num(0)

if __name__ == "__main__":
    doctest.testmod()
