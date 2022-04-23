# iterables, iterators, generators

# to date, we've seen examples of many different kinds of _iterable_ items in
# Python, things that exist to be looped over, for example:

x = [9, 8, 7]

# and we know that we can loop over this like:

for i in x:
    print(i)


# when we're doing the looping, Python is, behind the scenes, making a new kind
# of object called an _iterator_, which produces elements from the iterable
# object one-at-a-time.  we can actually also create these kinds of things
# ourselves as well, using the built-in `iter` function:

print()

y = iter(x)

# what can we do with iterators?  well, we can get objects from them
# one-at-a-time using the `next` function:

print(next(y))

# each repeated call gives us the _next_ object (the iterator remembers where
# it was in the process of working its way through the list).

# what happens when we run out of things in the list?  Python raises a special
# kind of exception (StopIteration)

print(next(y))
print(next(y))
# print(next(y))  # < -- here


# behind the scenes, when we loop over a list object, python actually makes a
# new iterator (effectively calling `iter` on the thing we're looping over) and
# repeatedly calls `next` on it until a StopIteration is produced

# so when we run the following piece of code:

for i in x:
    print(i)

# what's really happening behind the scenes is something like the following
# (but not exactly):

iterator = iter(x)
i = next(iterator)
while True:
    print(i)  # <- body of the loop above
    try:
        i = next(iterator)
    except StopIteration:
        break  # stop the loop


# iterators can also be looped over using `for`, but it's important to note
# that once we reach the end of the iterator, that iterator will generally not
# produce any more objects, for example:

x = [9, 8, 7]
y = iter(x)
for i in y:
    print('first', i)
for i in y:
    print('again', i)  # <- no agains get printed :O

# examples of iterators we've seen so far include enumerate and zip (and there
# are more: reversed, etc!)


# ok, so that's a lot of detail, and probably more than we need to know (it's
# nice that Python abstracts away the details of this operation for us and we
# don't have to look under the hood!), but the reason to talk about this here
# is to frame our main point of conversation for the day, which is that Python
# gives us ways to directly create iterators _without the need for an
# underlying collection like a list_.  this is a _really powerful_ idea, which
# we'll explore for the remainder of today's recitation.


# as our first real example of the day, let's consider writing our own little
# implementation of something like Python's range function (without some of the
# fancy features, but it's a start):


def list_range(start, stop):
    out = []
    while start < stop:
        out.append(start)
        start += 1
    return out


# now let's try testing it out...

#for i in list_range(0, 1_000_000_000):
#    print('yay', i)
#    if i > 10:
#        break

# what happened?!  why did we not seeing anything printed?

# python is spending that time _building a list_ by calling our function!  it's
# only after that list is created (which takes a lot of time and memory) that
# we can even start looping over it!

# but now we'll introduce a way that we can get around this by directly
# creating an iterator, without the need for an intermediate list!  in
# particular, the tool we'll use is called a _generator_, which is a nice way
# to create an iterator directly.  the syntax for a generator mirrors that of
# a normal function, but with a new keyword, yield.  now, instead of building
# up a list of elements, we're going to tell python to "yield" the elements one
# after another:

def gen_range(start, stop):
    while start < stop:
        yield start
        start += 1

# in general, we can convert a function that builds up a list (or set or...) of
# elements into a generator by:
#
#  * removing any initialization of the collection we would be building
#  * yielding elements instead of adding them to a collection

# now, let's look at what happens when we run this!

g = gen_range(0, 1_000_000_000)  # <- notice that this finishes right away!

# if we print g, we see that it is a generator, e.g.
#    <generator object gen_range at 0x7f43200cb580>

# and we can get items form it using `next`:

print(next(g))

# what is happening behind the scenes?  when we call the function gen_range,
# Python runs through the normal function call process, _EXCEPT_ that it
# doesn't actually start running the code yet!  so we get a new frame set up as
# normal (and we get `start` and `stop` bound there), but we don't actually run
# the body of `gen_range` yet.  instead, Python gives us a "generator iterator"
# object that references both the `gen_range` function and the new frame we've
# made (see diagram).

# we can add print statements to see what exactly is happening and when:

def gen_range(start, stop):
    print('START')
    while start < stop:
        print('HELLO1', start)
        yield start
        print('HELLO2', start)
        start += 1


# it's only when we call `next(g)` that we actually run any of the code!  we
# run until we find a `yield` statement, and then we pause the execution until
# `next` is called again, at which point we pick up the execution again and run
# until we see another yield, etc, etc, etc.

# we can also loop over the generator using `for`:

for i in g:
    print(i)
    if i > 10:
        break

# notice how quickly this happened, compared to our list example from above!
# it's not the case that generators are _always_ faster than lists, but it is
# the definitely the case that it saves us a lot of time in the example above,
# since we can avoid wasting time and memory building up a big list that we're
# eventually just going to loop over anyway.


# another interesting feature is that generators can be infinite (we couldn't
# do the following with a list!)

def inf_range(start):
    while True:
        yield start
        start += 1

#for i in inf_range(0):
#    print(i)


# generators using other generators!!!
# using generators, we can mimic the behaviors of a lot of built-in things (and
# others!)

def my_enumerate(x):
    ix = 0
    for elt in x:
        yield ix, elt
        ix += 1


def my_zip(x, y):
    x = iter(x)
    y = iter(y)
    while True:
        try:
            a = next(x)
            b = next(y)
        except StopIteration:
            return

        yield (a, b)

def interleave(x, y):
    x = iter(x)
    y = iter(y)
    while True:
        got_a = True
        try:
            a = next(x)
        except:
            a = None
            got_a = False

        got_b = True
        try:
            b = next(y)
        except:
            b = None
            got_b = False

        if got_a:
            yield a
        if got_b:
            yield b

        if not (got_a or got_b):
            return # no a or b val, quit!

def my_reversed(x):
    for i in range(len(x)-1, -1, -1):
        yield x[i]



# generators can also be recursive!  consider the following code, which is
# similar to code we've written a few times in 6.009 already:

def flatten(x):
    # here, x is an arbitrarily-nested list of numbers, i.e., a list of numbers
    # or other lists (when themselves contain numbers or other lists, and so
    # on).  we want to return a single flat list containing these numbers, but
    # with all nesting removed.
    out = []
    for elt in x:
        if isinstance(elt, list):
            out.extend(flatten(elt))
        else:
            out.append(elt))
    return out

# if, instead, we wanted a _generator_ that yielded all of these values, we
# could do that like so (note that the 'yield from' line is effectively the
# same as the commented-out lines that precede it)

def flatten(x):
    for elt in x:
        if isinstance(elt, list):
            #for i in flatten(elt):
            #    yield i
            yield from flatten(elt)
        else:
            yield elt


# generator expressions!!!

x = [i**2 for i in range(100)]  # <- this makes a list
x = (i**2 for i in range(100))  # <- this makes a generator!