import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    def __init__(self, name=""):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Symbol({self.name})'

class BinOp(Symbol):
    def __init__(self, name, loperand, roperand):
        Symbol.__init__(self, name)
        if isinstance(loperand, int):
            self.left = Num(loperand)
        elif isinstance(loperand, str):
            self.left = Var(loperand)
        else:
            self.left = loperand

        if isinstance(roperand, int):
            self.right = Num(roperand)
        elif isinstance(loperand, str):
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


class Sub(BinOp):
    precedence = 1
    sym = '-'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Sub', loperand, roperand)


class Mul(BinOp):
    precedence = 2
    sym = '*'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Mul', loperand, roperand)


class Div(BinOp):
    precedence = 2
    sym = '/'
    def __init__(self, loperand, roperand):
        BinOp.__init__(self, 'Div', loperand, roperand)


class Var(Symbol):
    precedence = float('inf')
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __add__(self, other):
        if isinstance(other, Var): # no type checking here
            return Add(self, other)
        else:
            return Error()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Var("{str(self.name)}")'


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
        return f'Num("{str(self.n)}")'


if __name__ == "__main__":
    doctest.testmod()
