from lab import Var, Num, Add, Sub, Mul, Div
z = Add(Var('x'), Sub(Var('y'), Num(2)))sub
repr(z) # notice that this result, if fed back into Python, produces an equivalent object.
str(z) # this result cannot necessarily be fed back into Python, but it looks nicer.
x = Var('x')
y = Var('y')
print(x+y)
z = x + y

# precedence problem

Mul(Var('x'), Add(Var('y'), Var('z'))) # left and/or right has lower precedence than current operator

a = Div(Var('x'), Div(Var('y'), Var('z')))
c = Div(Var('x'), Mul(Var('y'), Var('z')))
b = Sub(Var('x'), Add(Var('y'), Var('z')))
d = Sub(Var('x'), Sub(Var('y'), Var('z')))
