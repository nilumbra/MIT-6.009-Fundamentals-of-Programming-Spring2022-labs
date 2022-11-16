## 3)Conditional 
### Check Yourself
> Why is it important that only evaluates one of the branches? Can you think of a situation where evaluating both branches would be problematic?

My answer: For example, when two branches involve modifying some common states, evaluating two branches will cause unexpected results, as both branches modifying the set of states make the final state dependent on each other's execution.

## 3.1) Booleans and Comparisons
In order to implement , we will need a way to represent Boolean values in Carlae.
- `@t`
- `@f`

- `=?`true if all equal
- `>` true if decreasing
- `>=` true if nonincreasing

### Check Yourself
> `and` evaluates to true only if all of its arguments are true. So if we're evaluating all its arguments in order one- by-one, under what condition can we stop (and avoid evaluating the rest of the arguments)? What about `or`?"

Implement short-circuiting:
- `and`: evaluate to false if one is false
- `or`: evaluate to true if any one is true

### Check Yourself
> It could be nice to implement the comparison operations as special forms, too, so that they can short-circuit as well. If you want to do that, go ahead! But the test cases should pass either way.
