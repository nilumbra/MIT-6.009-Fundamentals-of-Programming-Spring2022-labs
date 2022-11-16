import sys
import turtle as pturtle  # Python's built-in turtle module

pturtle.speed("fastest")

penup = pturtle.penup
pendown = pturtle.pendown

def goto(x, y):
    pturtle.goto(x, y)

def new(width=500, height=500):
    pturtle.setup(width=width, height=height)
    pturtle.reset()

left = pturtle.left
forward = pturtle.forward

def getx():
    return pturtle.pos()[0]

def gety():
    return pturtle.pos()[1]

def geth():
    return pturtle.heading()

def heading(h):
    pturtle.setheading(h)

def turtle(funcname, args):
    func = getattr(sys.modules[__name__], funcname, None)
    if func is None or funcname == 'turtle' or not callable(func):
        raise NameError(f"unknown turtle function {funcname}")
    return func(*args)
