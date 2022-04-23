from instrument import show_recursive_structure

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
    return {word for word in hidden_words_helper(word) if word in ALL_WORDS}


def hidden_words_helper(word):
    """
    Helper function, returns all sequences of letters that can be created by
    removing 0 or more letters from the given word, even if the results are not
    valid words themselves.
    """
    pass
