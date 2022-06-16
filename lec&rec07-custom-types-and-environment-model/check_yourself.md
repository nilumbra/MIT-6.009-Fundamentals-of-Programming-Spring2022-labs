### Check Yourself:

> The structure of each of these classes' __init__ methods is likely to be almost the same (if not exactly the same). What does that suggest about how/where you should implement __init__?

> Take a look at the __repr__ and __str__ methods in Var and Num. What is the difference between them?


#### Parenthesization
> Think about the rules for parenthesization described above in terms of algebraic expressions and work through parenthesizing some example expressions by hand to get a feel for how these rules work. Do these rules seem to work in a general sense -- will they always work across different operations and across different levels of expression complexity? Why do they work? Why are subtraction and division treated differently from addition and multiplication?


> Importantly, you should implement this behavior without explicitly checking the type of self, self.left, or self.right.

Doing so will require having a way to get information about an instance's precedence. How can you store this information? And where should it be stored?