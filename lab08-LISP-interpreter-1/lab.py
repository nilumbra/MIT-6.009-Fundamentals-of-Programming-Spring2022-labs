#!/usr/bin/env python3
"""6.009 Lab 8: Carlae (LISP) Interpreter"""

import doctest
import math
from functools import reduce

# NO ADDITIONAL IMPORTS!


###########################
# Carlae-related Exceptions #
###########################


class CarlaeError(Exception):
    """
    A type of exception to be raised if there is an error with a Carlae
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class CarlaeSyntaxError(CarlaeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class CarlaeNameError(CarlaeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class CarlaeEvaluationError(CarlaeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    CarlaeNameError.
    """

    pass

############################
#       Environment        #
############################
class E:
  def __init__(self, initial_bindings=dict(), parent=None, name="global") -> None:
    self.bindings = initial_bindings
    self.parent = parent
    self.name = name

  def has(self, identifier):
    return identifier in self.bindings

  def get_binding(self, identifier):
    # print(f'get_binding({identifier} in environment: {self.name})')
    identifier = str(identifier)
    # print(f'get_binding({identifier} in environment: {self.name})')

    if identifier in self.bindings:
        return self.bindings[identifier]
    elif self.parent is not None:
        return self.parent.get_binding(identifier)
    else:
        raise CarlaeNameError(f'from E.get_binding: {identifier} is an undefined symbol')

  def set_binding(self, identifier:str, binded_val):
    if not isinstance(identifier, str):
        raise CarlaeSyntaxError(f'from E.get_binding: invalid variable type! Variable {identifier}  of type {type(identifier)} is not assignable!')
    # print(f'set binding of {identifier} in {self.name} to {binded_val}')

    self.bindings[identifier] = binded_val
    # print(f"Current environemnt {self.name} has bindings:", self.list_binding_keys(), end=None)

  def set_parent_environment(self, parent) -> None:
    self.parent = parent

  def list_binding_keys(self):
    return ','.join(self.bindings.keys())

############################
#      Function Class      #
############################
class UserDefinedFunction:
    def __init__(self, params=None, ast=None, env=None) -> None:
        self.params = params
        self.body = ast
        self.scope = env

    def apply(self, *arguments): # adding a calling scope? 
        global evaluate
        if len(arguments) != len(self.params):
            raise CarlaeEvaluationError("Function.call(): number of arguments is not consistent")
        
        bindings = {}
        for k, v in zip(self.params,arguments):
            bindings[k] = v 

        fn_env = E(bindings, self.scope)
        return evaluate(self.body, fn_env)
    
    def dry_run(self, *arguments) -> None:
        """
        For debugging purposes, print out the calling arguments and callee's body
        """
        if len(arguments) != len(self.params):
            raise CarlaeEvaluationError("Function.call(): number of arguments is not consistent")

        print("Function call:")
        print('Arguments: ', list(arguments))
        print('Body:', self.body)

    def __call__(self, *args, **kwds):
        pass


############################
# Tokenization and Parsing #
############################

def number_or_symbol(x):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Carlae
                      expression
    """

    def moveTemp():
        nonlocal tokens, temp
        if len(temp):
            tokens.append(''.join(temp))   
            temp = []

    tokens = []
    temp = []
    end = len(source)
    i = 0

    while i < end: 
        if source[i] == '(':
            moveTemp()
            tokens.append(source[i])
        elif source [i] == ')':
            moveTemp()
            tokens.append(source[i])
        elif source[i] not in [' ', '\n']: 
            if source [i] == '#':
                moveTemp()
                while i < end and source[i] != '\n': # skip the EOL/EOF if encounter #
                    i += 1 # 
                continue
            else: # good charaters
                temp.append(source[i])
        else: # space \n, 'flush' temp
            moveTemp()
        i += 1            
    
            
    moveTemp()
    # print(f'tokenized as: {tokens}')
    return tokens


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    def parse_expr(i):
        """
        Return (parsed_expression: List<String>, next_index: Integer)
        """
        nonlocal end, open
        expr = []

        # if i == end - 1: # if single token, e.g. ['2']
        #     return tokens[i] 

        while i < end:
            if tokens[i] == '(': # start read an S-expression
                open += 1
                parsed_expr, i = parse_expr(i+1) # start parsing from next token
                expr.append(parsed_expr)
            elif tokens[i] == ')': # end of curret S-expression
                open -= 1
                return expr, i
            else: # if is atomic expression
                if tokens[i] in ['function', ':=']:
                    if i - 1 < 0 or tokens[i - 1] != '(':
                        raise CarlaeSyntaxError("CarlaeSyntaxError: malformed S-expression! Hint: special form S-expressions expect an open parenthesis before keywords!")

                expr.append(number_or_symbol(tokens[i]))
            
            i+=1
        
        # assert i == end, f'Expect i == {end}, but i == {i}'

        return expr[0] if len(expr) == 1 else expr, end  # when this state is reach, i should always be <end>

    
    end = len(tokens)
    open = 0

    parsed, i = parse_expr(0)
    if open != 0:
        raise CarlaeSyntaxError('CarlaeSyntaxError: parenthesis mismatch!')
    # print(f'syntax tree: {parsed}')
    return parsed


######################
# Built-in Functions #
######################


carlae_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": math.prod,
    "/": lambda args: 1 / args[0] if len(args) == 1 else reduce(lambda x, y: x / y, args) 
}

__builtin__ = E(carlae_builtins, None, 'carlae_builtins') 
#  lambda args: args[0] if len(args) == 1 else  if 
__global__ = E({}, __builtin__)

##############
# Evaluation #
##############

def evaluate(tree, env=None):
    """
    Evaluate the given syntax tree according to the rules of the Carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    >>> evaluate("+ 2 3")
    5
    >>> evaluete("+ 2 (- 3 4)")                     
    1
    >>> evaluate("- 3.14 1.14 1")
    1.0000000000000004
    >>> evaluate("(* 5 (+ 3 1))")
    20
    >>> evaluate("/ 2 2")
    1.0
    >>> evaluate("/ 1 2 2")
    0.25
    """
    global __global__
    if env is None:
        # assert False, "This should never be called! (for now)"
        env =  __global__ # the default empty env has __builtin__ as its parent environment
    
    if isinstance(tree, int):
        return int(tree)
    elif isinstance(tree, float):
        return float(tree)
    elif isinstance(tree, list): # if is S-expression
        if tree[0] == ':=':
            if len(tree) != 3:
                raise CarlaeSyntaxError(f'evaluate(): invalid assignment syntax!! Expect 2 operands but {len(tree) - 1} are given.')
            
            if isinstance(tree[1], list): # if is function simple notation
                """
                I'm making up an AST on the fly here. This seems awkward. Is there a better way?
                """
                val = evaluate(['function', tree[1][1:], tree[2]], env) 
                env.set_binding(tree[1][0], val) # e.g. (:= -->(square x)<-- (* x x)
            else: 
                val = evaluate(tree[2], env)
                env.set_binding(tree[1], val) # do assignement
            return val

        elif tree[0] == 'function': # this part should be abstract to another function, say, createUserDefinedFunction
            if len(tree) != 3:
                raise CarlaeEvaluationError("evalutate(): invalid function definition")
            if not all(map(lambda param: isinstance(param, str), tree[1])):
                # print(tree[1])
                raise CarlaeEvaluationError(f'evaluate(): function parameter definition cannot only be str type')
            
            # if not isinstance(tree[2], list): # this is not needed e.g. (call (function () 2))
            #     raise CarlaeEvaluationError('evaluate(): malformed function body!')

            userFn = UserDefinedFunction(tree[1], tree[2], env)
            return userFn

        else: # function call
            fn = evaluate(tree[0], env) # existence is ensured
            
            if not hasattr(fn, '__call__'):
                raise CarlaeEvaluationError(f'evalauate() throws CarlaeEvaluationError: {fn} is not a valid function')

            if isinstance(fn, UserDefinedFunction):# user defined function
                # fn.dry_run([evaluate(el, env) for el in tree[1:]])
                return fn.apply(*[evaluate(el, env) for el in tree[1:]])
            else:
                return fn([evaluate(el, env) for el in tree[1:]])
        # else:
        #     raise CarlaeNameError(f'evaluate() throws CarlaeNameError: {tree[0]} is not a built-in function!')
    else:
        # raise CarlaeNameError(f'evaluate() throws CarlaeNameError: {tree[0]} is not a built-in function!')
        # raise NotImplementedError(f'{tree} symbols are not supported yet!')
        return env.get_binding(tree)
        
def result_and_env(tree, env=None):
    """
    Evaluate the given syntax tree and returns
        (result, environment)
    where
        result: evaluate(tree) 
        environment: the environment the expression is evaluated
    """
    global __builtin__
    # if and environment is given, the expression should be evaluated in that environment
    if env:
        res = evaluate(tree, env)
    else:
        #create a new environment and evaluate the expression in that enviroment
        env = E({}, __builtin__)
        res = evaluate(tree, env)
    
    return (res, env)

if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    # global_env = E({}, carlae_builtins)
    env = None
    while True:
        expr = input('in>')
        if expr == 'EXIT':
            break
        try:
            # res, global_env = result_and_env(parse(tokenize(expr)))
            if env is None:
                res, env = result_and_env(parse(tokenize(expr)))
            else:
                res, env = result_and_env(parse(tokenize(expr)), env)
            print(f' out> {res}')
                # print(f' out> {result_and_env(parse(tokenize(expr)), global_env)}')
        except CarlaeError as e:
            print(e)
        except NotImplementedError as e:
            print(e)

