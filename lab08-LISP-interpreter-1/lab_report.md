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