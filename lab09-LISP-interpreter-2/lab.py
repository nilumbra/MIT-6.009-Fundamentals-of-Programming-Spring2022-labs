"""6.009 Lab 9: Carlae Interpreter Part 2"""

import sys
sys.setrecursionlimit(10_000)

# KEEP THE ABOVE LINES INTACT, BUT REPLACE THIS COMMENT WITH YOUR lab.py FROM
# THE PREVIOUS LAB, WHICH SHOULD BE THE STARTING POINT FOR THIS LAB.
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
  def __init__(self, initial_bindings=dict(), parent=None, name="anoynomous") -> None:
    self.bindings = initial_bindings
    self.parent = parent
    self.name = name

  def has(self, identifier):
    return identifier in self.bindings

  def get_binding(self, identifier):
    # print(f'get_binding({identifier} in environment: {self.name})... ', end="")
    identifier = str(identifier)
    # print(f'get_binding({identifier} in environment: {self.name})')

    if identifier in self.bindings:
      # print("found!\n")
      return self.bindings[identifier]
    elif self.parent is not None:
      # print("not found!")
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
      raise CarlaeEvaluationError("Function.apply(): number of arguments is not consistent")
  
    bindings = {}
    for k, v in zip(self.params,arguments):
        bindings[k] = v 

    fn_env = E(bindings, self.scope)
    return evaluate(self.body, fn_env) ## MAKE SURE YOU UNDERSTAND THIS
  
  def dry_run(self, *arguments) -> None:
    """
    For debugging purposes, print out the calling arguments and callee's body
    """
    if len(arguments) != len(self.params):
        raise CarlaeEvaluationError("Function.call(): number of arguments is not consistent")

    print("Function call:")
    print('Arguments: ', list(arguments))
    print('Body:', self.body)

  def __call__(self, *args):
    return self.apply(*args)


class Pair:
  def __init__(self, head=None, tail=None) -> None:
    self.head = head
    self.tail = tail
  
  def __repr__(ptr) -> str:
    return f'({ptr.head}, {ptr.tail})'

  def last(self):
    """
      Assume self represents a list,
      return the reference to the last element of self
    """
    assert _isList([self]), "Pair.last: cannot get the last of a non-list!"
    ptr = self
    while ptr and ptr.tail:
      ptr = ptr.tail
    
    return ptr

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
def short_circuit(tuples, cond, env, to=False, t="comp") -> bool:
  """
  tuple: a set of numbers or booleans
  cond: the condition to shortcircuit, should be a lambda accepting two arguments
  bool: shortcircuit default value
  """
  for i in range(0, len(tuples) - 1*(t=='comp')):
    if t == 'comp':
      if cond(evaluate(tuples[i], env), evaluate(tuples[i+1], env)):
        return to
    elif t == 'comb': ## boolean combinators
      if cond(evaluate(tuples[i], env)):
        return to
  return not to

def _list(args, env):
  if len(args) == 0:
    return carlae_literals['nil']

  tail = carlae_literals['nil']
  i = len(args) - 1
  while i >=0:
    head = Pair(evaluate(args[i], env), tail)
    tail = head
    i -= 1

  # print(head)
  return head

def _pair(args):
  if len(args) != 2:
    raise CarlaeEvaluationError("_pair(): built-in function pair takes exactly 2 arguments")
  return Pair(*args)

def _isList(args):
  if len(args) != 1:
    raise CarlaeEvaluationError("isList(): built in function list? takes exactly 1 argument.")
  
  obj = args[0]
  return obj == carlae_literals['nil'] or (isinstance(obj, Pair) and _isList([obj.tail]))

def _length(args):
  if len(args) != 1 or not _isList(args):
    raise CarlaeEvaluationError("_length(): built in function length takes exactly 1 list as argument.")
  
  ptr = args[0]
  if ptr == carlae_literals['nil']: return 0
  
  i = 1
  while (ptr:=ptr.tail):
    i += 1
  return i

def _nth(args):
  if len(args) != 2 or not isinstance(args[1], int) or (not _isList([args[0]]) and not isinstance(args[0], Pair)):
    raise CarlaeEvaluationError("_nth(): built in function nth takes exactly 2 arguments. See usage: nth LIST INDEX.")

  # ptr is ensured to be a Pair
  ptr, i = args 
  if not _isList([ptr]):
    if i == 0: # LIST is a pair 
      return ptr.head
    else: # LIST is a pair but the index is not 0
      raise CarlaeEvaluationError("_nth(): positive index does not apply to Pair!!")
  
  # ptr is a list
  if ptr == carlae_literals['nil']:
    raise CarlaeEvaluationError("_nth(): empty list is not indexable!!")

  while i > 0:
    ptr = ptr.tail
    if ptr == carlae_literals['nil']:
      raise CarlaeEvaluationError("_nth(): index out of range!!")

    i -= 1
  return ptr.head

def _clone_list(args):
  """
  Assume arg is a list, return a clone of args

  Usage: _clone_list([LIST])
  """
  assert len(args) == 1
  L = args[0]

  assert _isList([L])
  l = _length([L])
  if l == 0:
    return L # empty list is a singleton, just return it

  first = Pair(L.head, None)
  ptr = first
  while (L := L.tail):
    ptr.tail = Pair(L.head)
    ptr = ptr.tail

  return first

def _concat(args):
  if (n:= len(args)) == 0: # produce an empty list in concat is called with no arguments 
    return carlae_literals['nil']

  if any(map(lambda l: not _isList([l]), args)): # if any args is not a list
    raise CarlaeEvaluationError("concat(): cannot concat non-list to list(s)!")
  
  # print("Concatenating: ", end="")
  # for l in args:
  #   print(l, end=" ")
  # print()

  first = _clone_list([args[0]])

  last = first.last() if _length([first]) else first

  for L in args[1:]:
    # traverse to ptr's last element, call it last
    if _length([L]) == 0: # 
      continue
    
    if _length([last]) == 0: # if last is empty use L as head
      last = _clone_list([L])
      first = last
      continue
      
    last.tail = (_L := _clone_list([L])) # # append
    last = _L.last()
     
  return first

def _map(args):
  """
  (map FUNC LIST)
  """
  if len(args) != 2:
    raise CarlaeEvaluationError("map(): map takes exactly 2 arguments.")
  
  if not hasattr(args[0], '__call__') or not _isList([args[1]]):
    raise CarlaeEvaluationError("map(): argument types mismatch. Usage: (map FUNC LIST)")
  
  if _length([args[1]]) == 0:
    return carlae_literals['nil']
  
  fn, L = args

  isArr = not isinstance(fn, UserDefinedFunction)

  first = Pair(fn([L.head] if isArr else L.head))
  ptr = first
  while (L := L.tail):
    # print(fn([L.head] if isArr else L.head))
    ptr.tail = Pair(fn([L.head] if isArr else L.head))
    ptr = ptr.tail

  return first

def _filter(args):
  """
  (filter FUNC LIST)
  """
  if len(args) != 2:
    raise CarlaeEvaluationError("filter(): filter takes exactly 2 arguments.")
  
  if not hasattr(args[0], '__call__') or not _isList([args[1]]):
    raise CarlaeEvaluationError("filter(): argument types mismatch. Usage: (filter FUNC LIST)")

  if _length([args[1]]) == 0:
    return carlae_literals['nil']

  fn, L = args
  first = None
  ptr = None
  while L:
    if fn(L.head):
      if first is None:
        first = Pair(L.head)
        ptr = first
      else: 
        ptr.tail = Pair(L.head)
        ptr = ptr.tail
    L = L.tail

  return first


def _reduce(args):
  """
  (reduce FUNC LIST INITVAL)
  """
  if len(args) != 3:
    raise CarlaeEvaluationError("reduce(): reduce takes exactly 3 arguments.")
  
  fn, L, initVal = args

  if not hasattr(fn, '__call__') or not _isList([L]):
    raise CarlaeEvaluationError("reduce(): argument types mismatch. Usage: (reduce FUNC LIST INITVAL)")

  if _length([L]) == 0:
    return initVal
  
  isArr = not isinstance(fn, UserDefinedFunction)

  while L:
    initVal = fn([initVal, L.head]) if isArr else fn(initVal, L.head)
    L = L.tail
  
  return initVal


carlae_builtins = {
  "+": sum,
  "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
  "*": math.prod,
  "/": lambda args: 1 / args[0] if len(args) == 1 else reduce(lambda x, y: x / y, args),
  "=?": lambda args, env: short_circuit(args, lambda a, b: a != b, env),
  ">": lambda args, env: short_circuit(args, lambda a, b: a <= b, env),
  ">=": lambda args, env: short_circuit(args, lambda a, b: a < b, env),
  "<": lambda args, env: short_circuit(args, lambda a, b: a >= b, env),
  "<=": lambda args, env: short_circuit(args, lambda a, b: a > b, env),
  "and": lambda args, env: short_circuit(args, lambda a: not a, env, t="comb"),
  "or": lambda args, env: short_circuit(args, lambda a: a, env, to=True, t="comb"),
  "not": lambda args, env: not evaluate(args[0], env),
  "pair": _pair,
  "head": lambda p: p.head,
  "tail": lambda p: p.tail,
  "list": _list,
  "clone_list": _clone_list,
  "last": lambda args: args[0].last(),
  "list?": _isList,
  "length": _length,
  "nth": _nth,
  "concat": _concat,
  "map": _map,
  "filter":_filter,
  "reduce": _reduce,
}

carlae_literals = {
  '@t': True,
  '@f': False,
  'nil': None
}

__builtin__ = E(carlae_builtins, None, 'carlae_builtins') 
#  lambda args: args[0] if len(args) == 1 else  if 
__global__ = E({}, __builtin__, '__global__')

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
  if env is None:
    # assert False, "This should never be called! (for now)"
    env =  E({}, __builtin__, name="anoynmous") # the default empty env has __builtin__ as its parent environment

  if isinstance(tree, int):
    return int(tree)
  elif isinstance(tree, float):
    return float(tree)
  elif isinstance(tree, list): # if is S-expression
    # The following will throw any error!!
    # in>()
    # tokenized as: ['(', ')']
    # syntax tree: []
    if len(tree) == 0:
      raise CarlaeEvaluationError(f'evaluate(): invalid S-expression! () is not a valid S-expression')

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
    elif tree[0] == 'if': #(if COND TRUE_EXP FALSE_EXP)
      if len(tree) != 4:
        raise CarlaeEvaluationError("evaluate(): invalid conditional expression! Conform to syntax (if COND TRUE_EXP FALSE_EXP)")

      if evaluate(tree[1], env):
        return evaluate(tree[2], env)
      else:
        return evaluate(tree[3], env)
    else: # function call
      fn = evaluate(tree[0], env) # existence is ensured
      
      if not hasattr(fn, '__call__'):
        raise CarlaeEvaluationError(f'evalauate() throws CarlaeEvaluationError: {fn} is not a valid function')

      #####################################
      ##### USER DEFINED FUNCTIONS
      if isinstance(fn, UserDefinedFunction):
        # fn.dry_run([evaluate(el, env) for el in tree[1:]])
        return fn.apply(*[evaluate(el, env) for el in tree[1:]])

      #####################################
      ##### BUILT IN FUNCTIONS
      else: 
        # Comparison and Boolean combinators enforces special constraints on the number of arguments
        if (func_name:=tree[0]) in ['=?', '>', '>=', '<', '<=', 'and', 'or', 'not']: 
          if func_name != 'not' and len(tree) < 3:
            raise CarlaeEvaluationError("evaluate(): Comparisons or Boolean combinators expect at least 2 arguments")
          elif func_name == 'not': 
            if len(tree) != 2:
              raise CarlaeEvaluationError("evaluate(): not keyword expects exactly 1 arguments")
          return fn(tree[1:], env) # need to pass an environment, because we need to support short-circuiting!
        elif func_name in ['head', 'tail']: # built in functions to support Pair
          if len(tree) != 2:
            raise CarlaeEvaluationError("evaluate(): head/tail expects exactly one arugment!")
          elif not isinstance((pair:=evaluate(tree[1], env)), Pair):
            raise CarlaeEvaluationError("evaluate(): head/tail expects a Pair object!")
          return fn(pair)
        elif func_name == 'list':
          return fn(tree[1:], env)

        return fn([evaluate(el, env) for el in tree[1:]]) # 

      # else:
      #     raise CarlaeNameError(f'evaluate() throws CarlaeNameError: {tree[0]} is not a built-in function!')
  else: # symbols
    #################### Literals Definitions Come First##################
    if (symbol:=tree) in carlae_literals:
      return carlae_literals[symbol]
    ######################################################################
    return env.get_binding(symbol)
        
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
        res, env = result_and_env(parse(tokenize(expr)), __global__)
      else:
        res, env = result_and_env(parse(tokenize(expr)), env)
      print(f' out> {res}')
        # print(f' out> {result_and_env(parse(tokenize(expr)), global_env)}')
    except CarlaeError as e:
      print(e)
    except NotImplementedError as e:
      print(e)

