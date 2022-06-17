from lab import Var, Num, Add, Sub, Mul, Div

##### Test Display #####
z = Add(Var('x'), Sub(Var('y'), Num(2)))sub
repr(z) # notice that this result, if fed back into Python, produces an equivalent object.
str(z) # this result cannot necessarily be fed back into Python, but it looks nicer.
x = Var('x')
y = Var('y')
print(x+y)
z = x + y

# test exponents 
x = Var('x')
y = x ** 3
print(x)


# Test parenthesization by precedence works well

Mul(Var('x'), Add(Var('y'), Var('z'))) # left and/or right has lower precedence than current operator

a = Div(Var('x'), Div(Var('y'), Var('z')))
c = Div(Var('x'), Mul(Var('y'), Var('z')))
b = Sub(Var('x'), Add(Var('y'), Var('z')))
d = Sub(Var('x'), Sub(Var('y'), Var('z')))


# Test operations between Num, Var, and built in type such as Integer and float works
Num(3) + 'x'


3 - Num(2)
str(_)

3 * Var('x')
str(_)

3 / Var('x')
str(_)


##### Test Derivatives #####

b = Num(5) # constant.deriv('x') == 0
b.deriv('x')

x = Var('x') # 'x'.deriv('x') == 1
x.deriv('x')

y = Var('y') # 'x'.deriv('x') == 1
y.deriv('x')


# test addition
x = Var('x')
y = Var('y')
x_add_y = x + y 
x_add_y.deriv('x')
str(_)

# test multiplication
x = Var('x')
y = Var('y')
z = 2*x - x*y + 3*y
print(z.deriv('x'))

z = 2 * Var('x') * Var('x')
print(z.deriv('x'))
# (2 * x).deriv('x')
# str(_)
# (x * y).deriv('x')
# str(_)
# (3 * y).deriv('x')
# str(_)

# test division
u = Var('x') + 1
v = 2 * Var('x') * Var('x')



