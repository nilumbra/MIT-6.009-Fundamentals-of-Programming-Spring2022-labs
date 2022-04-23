class LinkedList:
    def __init__(self, elt, next_node):
        self.elt = elt
        self.next_node = next_node

    def _find_node(self, index):
        if index < 0:
            # TODO: implement support for negative indices!
            raise IndexError("negative indices are not supported")
        if index == 0:
            return self
        if self.next_node is None:
            raise IndexError("index out of range")
        return self._find_node(index - 1)

    def __getitem__(self, index):
        return self._find_node(index).elt

    def __setitem__(self, index, value):
        self._find_node(index).elt = value

    # TODO: to allow looping over our linked lists, define __iter__(self).
    # this should be a generator, yielding the elements from the linked list in
    # order.  this is used when we say, for example, "for i in x: ..."

    # TODO: define __len__(self), which should return the length of the linked
    # list when we call, for example, "len(x)"

    # TODO: define __delitem__(self, index), which removes a node from the
    # linked list when we run, for example, "del x[2]"

    # TODO: define append(self, value), which adds a new node to the end of the
    # linked list containing the given element


if __name__ == '__main__':
    x = LinkedList(4,
            LinkedList(8,
                LinkedList(15,
                    LinkedList(16,
                        LinkedList(23,
                            LinkedList(42, None))))))