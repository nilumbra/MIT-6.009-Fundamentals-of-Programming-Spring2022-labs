import doctest

class LinkedList:
    def __init__(self, elt, next_node=None):
        self.elt = elt
        self.next_node = next_node

    def _get_node(self, index):
        if index < 0:
            return self._get_node(index + len(self))

        if index == 0:
            return self

        if self.next_node is None:
            raise IndexError("LinkedList index out of range")

        return self.next_node._get_node(index-1)

    def __getitem__(self, index):
        """
        >>> x = LinkedList(9, LinkedList(8, LinkedList(7)))
        >>> x[2]
        7
        >>> x[1]
        8
        >>> x[100]
        Traceback (most recent call last):
            ...
        IndexError: LinkedList index out of range
        """
        return self._get_node(index).elt

    def __setitem__(self, index, value):
        """
        >>> x = LinkedList(9, LinkedList(8, LinkedList(7)))
        >>> x[2] = 'cat'
        >>> x
        LinkedList(9, LinkedList(8, LinkedList('cat', None)))
        >>> x[100] = 'dog'
        Traceback (most recent call last):
            ...
        IndexError: LinkedList index out of range
        """
        self._get_node(index).elt = value

    def __repr__(self):
        return f'LinkedList({self.elt!r}, {self.next_node!r})'

    def __iter__(self):
        yield self.elt
        if self.next_node is not None:
            yield from self.next_node

    def __len__(self):
        for ix, _ in enumerate(self):
            pass
        return ix + 1

    def append(self, elt):
        self._get_node(len(self) - 1).next_node = LinkedList(elt)

    def __delitem__(self, index):
        preceding_node = self._get_node(index-1)
        to_delete = preceding_node.next_node
        preceding_node.next_node = to_delete.next_node
        to_delete.next_node = None


if __name__ == '__main__':
    doctest.testmod()
    x = LinkedList(4, LinkedList(8, LinkedList(15, LinkedList(16, LinkedList(23, LinkedList(42))))))