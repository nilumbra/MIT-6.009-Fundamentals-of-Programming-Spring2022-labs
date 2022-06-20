from lab import Var, Num, Add, Sub, Mul, Div, tokenize, expression, Pow

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


##### Test Simplification #####
# 1. Any binary operation on two numbers should simplify to a single number containing the result.
x = Num('3')
y = Num('4')
(x + y).simplify()
print(_)

(x - y).simplify()
print(_)

(x * y).simplify()
print(_)

(x / y).simplify()
print(_)

# 2. Adding 0 to (or subtracting 0 from) any expression E should simplify to E.
z = Var('x') + 0
print(z)
print(z.simplify())

z = Var('x') - 0
print(z.simplify())

z = 0 + Var('x')
print(z.simplify())

# 3. Multiplying any expression E by 0 should simplify to 0, and 
#    Dividing 0 by any expression E should simplify to 0
x = Var('x')
z = x * 0
print(z.simplify())

x = Var('x')
z = 0 / x
print(z.simplify())


# 4. Multiplying or dividing any expression E by 1 should simplify to E.
x = Var('x')
z = x * 1
print(z.simplify())

x = Var('x')
z = x / 1
print(z.simplify())

# 5. A single number or variable always simplifies to itself.


# merge simplification
ep1 = Num(2) + Num(1) + Var('x') * 0
ep2 = Var('x') * 0 + Var('y') * 1

z = ep1 - ep2 


x = Var('x')
y = Var('y')
z = 2*x - x*y + 3*y
print(z.simplify())
print(z.deriv('x').simplify())

##### Test Evaluation #####
x = Var('x')
y = Var('y')
z = 2*x - x*y + 3*y
m = {'x': 1, 'y': 2}
z.eval(m)


##### Test Parse #####
tl = tokenize("(x * (2 + 3))")

longer = "(1 + (4 + 5 + 2) - 3) + (6 + 8))"
tl_longer = tokenize(longer)
parse(tl_longer)
str(_)


longer1 = "(1 + 4 + 5 + 2 - 3 + 6 + 8)"
tl_longer1 = tokenize(longer1)
parse(tl_longer1)
str(_)

longer2 = "(a * ((v - x - (-8 - 2) + G / 6 - (P - -2) - w) * b / -8 + -3) / s / (s / (7 * e * (6 - 10 - (K * 8 + -6 + V - (S + I - w))) / ((4 - q + B) / (-7 + c / X) - 7 * m / b)) + 9))"
tl_longer2 = tokenize(longer2)
parse(tl_longer2)
str(_)

##### Test Pow #####

2 ** Var('x')

a = (2 ** Num(3)) ** Num(4)

# parsing 
x = expression('(x ** 2)')

# derivative
x.deriv('x')

print(x.deriv('x').simplify()) # 2 * x
print(Pow(Add(Var('x'), Var('y')), Num(1))) # (x + y) ** 1
print(Pow(Add(Var('x'), Var('y')), Num(1)).simplify()) # x + y
