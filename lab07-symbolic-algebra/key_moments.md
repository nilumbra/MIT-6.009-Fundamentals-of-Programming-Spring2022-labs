### No Explicit type checking
Instead of explicitly checking the types of our objects and determining our behavior based on those results, our goal is to use Python's own mechanism of method/attribute lookup to implement these different behaviors without the need to do any type checking of our own.

**Solution:** Using `self` key word cleverly. For example, define a method `m` in `Parent` class and access `self.a`, by not overriding the method in child class, and by defining a class variable `self.a` instead of an instance variable `self.a` in the `Child` class, a call as `child.m()` will access the class variable `Child.a`, by the Python's own mechanism of attribute lookup.

Reference: https://blog.peterlamut.com/2018/11/04/python-attribute-lookup-explained-in-detail/

and https://stackoverflow.com/questions/29565062/access-child-class-variables-in-parent-class



### 7) Derivatives
Even though it may not be obvious from looking at first glance, these mathematical definitions are recursive! That is to say, partial derivatives of compound expressions are defined in terms of partial derivatives of component parts, which may suggest strategies for implementing these rules in your program!


### 8) Simplification
- Implement additive/multiplicative identity in `BinOp` class. 