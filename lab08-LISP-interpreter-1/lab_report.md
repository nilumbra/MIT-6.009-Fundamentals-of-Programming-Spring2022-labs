## 2.1) LISP and Carlae
### Syntax
Very, very simple.
- Atomic expression: numbers(e.g. 4) and symbols(e.g. variable names, operators)
- S-expression: an opening bracket (, followed by zero or more expressions, followed by a closing round bracket  ). The first subexpression determines what the S-expression means
  - s-expression that starts with a key words, e.g. (*function* ...) is a *special form*

## 4) Tokenizer
Q: What should be the result of `tokenize("(cat (dog (tomato)))")`? \
A: ["(", "cat", "(", "dog", "(", "tomato", ")", ")", ")"]


<br>
Q: Waht should be the result of tokenizing the following expression?

```#add the numbers 2 and 3
(+ # this expression
 2     # spans multiple
 3 # lines

)
```
A: ["(", "+", "2", "3", ")"]

### Check yourself
> Note that this is similar in many ways to the tokenizer we wrote as part of lab 7. What are the key similarities and key differences? How can we modify that tokenizer to work in this context?

output: a list of tokens that make up an expression \
diff: categories of tokens? \
key diff: The whitespace characters serve to delineate the boundary between tokens in carlae whereas in lab 7, whitesapce serves no functional purpose at all to the arithmitic expressions.


## 5) Parser
- Similar to the little language I created for symbolic algebra in the previous lab
- Difference:
  - Symbolic algebra language always had exactly two subexpression to parse inside of parentheses, S-expressions can contain arbirarily many subexpressions
## 5.1) Examples
- What should be the result of calling `parse` the output from the first concept question above?
- What should be the result of calling `parse(['2'])`? (`2`)
- What should be the result of calling `parse(['x'])`? (`'x'`)
- What should be the result of calling `parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')'])`? (`['+', 2, ['-', 5, 3], 7, 8]`]


## 6) Evaluation
**Important!! D&C**
> We'll hold off on implementing variables, lists, conditionals, and functions for a little while; for now, we'll start by implementing a small calculator that can handle the and operations.
## 6.1)Evaluator: Calculator


A recursive evaluation procedure for the syntax tree is defined as follows:
- If the expression is a symbol representing a name in `carlae_buildins`, it should return the associated object.
- If the expression is a number, it should return that number
- If the expression is a list(representing an S-expression), each of the elements in the list should be evaluated, and the result of evaluating the first element (a function) should be called with the remaining elements passed in as arguments. The overall result of evaluating such a function is the return value of that function call

## 6.3)Adding Support for Variables
- `:=` differs from the function calls in that it does not evaluate the name that follows; it only evaluates the expression that follows the name.

## 6.4)Enviroments

### Check yourself
> What information should be stored as instance attributes of this class? What kind of methods should the class support

## 6.5) Evaluator Changes
### 6.5.1)Changes to `evaluate`
- make sure that evaluate handles the := keyword properly, evaluating the given expression and storing the result in the environment that was passed to `evaluate`.
- modify the way symbols are handled in `evaluate`, so that if the symbol exists as a key in the environment, `evaluate` returns the associated value

### 6.6)Environments, Test Cases, and the REPL
```py
def result_and_env(tree: CarlaeSynatxTree)->(result,environment): 
```

`result_and_env`: should always return the environment in which the expression was evaluated

### 6.7.1)Defining functions
- A `function` expression takes the form: `(function (PARAM1 PARAM2 ...) EXPR)`
- The result of evaluating such an expression should be an object representing that function.
- Need to keep track of:
  - the code representing the body of the function
  - the names of the function's parameter 
  - a pointer to the environment in which the function was defined, i.e. its enclosing environment
- A user-defined function should be represented by a **class**

#### Check your self
> What information should be stored as instance attributes of this class? What kind of methods should the class support?

### 6.7.2)Calling Functions
- evaluate all of the arguments to the function in the current environment(from which the function is being called).
- make a new environment whose parent is the function's enclosing environment(this is called `lexical scoping`)
- in that new environment, bind the function's parameters to the arguments that are passed to it
- evaluate the body of the function in that new environment

#### Exception 
- if we try to call something that is not a function 
- if we try to call a function with the incorrect number of arguments passed in, a CarlaeEvaluationError should be raised ✅


### 6.7.4)Changes to evaluate
#### Check your self
> How difficult was it to add the special form? And how much did it complicate your code? Next week, we will be adding several new special forms to the language, so it is worth thinking ahead to see if there are ways of reorganizing your code to make adding new special forms easier


### Examples
```Lisp
(:= square (function (x) (* x x))) # define func and assignment
`(square 2)` # calling function

```

#### Calling Functions

