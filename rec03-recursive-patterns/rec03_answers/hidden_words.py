with open("words.txt") as f:
    ALL_WORDS = set(f.read().splitlines())


def hidden_words(word):
    """
    Return all the words that are hidden in the current word. i.e. if you cross
    off some letters of the current word, does it lead to anoter word. Return a
    list of all such hidden words.
    >>> result = hidden_words("cat")
    >>> expected =  {'cat', 'at'}
    >>> result == expected
    True
    """
    return hidden_words_helper(word) & ALL_WORDS


def hidden_words_helper(word):
    """
    Helper function, returns all sequences of letters that can be created by
    removing 0 or more letters from the given word, even if the results are not
    valid words themselves.
    """
    results = {word}
    for ix in range(len(word)):
        results |= hidden_words_helper(word[:ix] + word[ix+1:])
    return results


# alternative structure:
def hidden_words_helper(word):
    if word == '':
        return {''}

    without_first_letter = hidden_words_helper(word[1:])
    return without_first_letter | {word[0] + w for w in without_first_letter}

print(hidden_words_helper('cats'))
print(hidden_words('cats'))

import doctest
doctest.testmod()
