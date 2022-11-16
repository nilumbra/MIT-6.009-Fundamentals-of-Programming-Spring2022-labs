#!/usr/bin/env python3
"""6.009 Lab 8: Carlae (LISP) Interpreter"""

import doctest

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
                        raise CarlaeSyntaxError("Malformed S-expression: special form S-expressions expect an open parenthesis before keywords!!")
            
                expr.append(number_or_symbol(tokens[i]))
            
            i+=1
        
        # assert i == end, f'Expect i == {end}, but i == {i}'

        return expr[0] if len(expr) == 1 else expr, end  # when this state is reach, i should always be <end>

    
    end = len(tokens)
    open = 0

    parsed, i = parse_expr(0)
    if open != 0:
        raise CarlaeSyntaxError('Parenthesis mismatch!')
    return parsed


######################
# Built-in Functions #
######################


carlae_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
}


##############
# Evaluation #
##############


def evaluate(tree):
    """
    Evaluate the given syntax tree according to the rules of the Carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    raise NotImplementedError


if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    pass
