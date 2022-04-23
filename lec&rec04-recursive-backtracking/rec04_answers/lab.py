# TENT PACKING

# Pack a tent with different sleeping bag shapes leaving no empty squares
#
# INPUTS:
#   tent_size = (rows, cols) for tent grid
#   rock_squares = set of (r, c) tuples giving location of rocks
#   bag_list = list of sets, each decribing a sleeping bag shape
#      Each set contains (r, c) tuples enumerating contiguous grid
#      squares occupied by the bag, coords are relative to the upper-
#      left corner of the bag.  You can assume every bag occupies
#      at least the grid (0,0).
#
# Example bag_list entries:
#      vertical 3x1 bag: { (0,0), (1,0), (2,0) }
#      horizontal 1x3 bag: { (0,0), (0,1), (0,2) }
#      square bag: { (0,0), (0,1), (1,0), (1,1) }
#      L-shaped bag: { (0,0), (1,0), (1,1) }
#      C-shaped bag: { (0,0), (0,1), (1,0), (2,0), (2,1) }
#      reverse-C-shaped bag: { (0,0), (0,1), (1,1), (2,0), (2,1) }
#
# OUTPUT:
#   None if no packing can be found; otherwise a list giving the
#   placement and type for each placed bag expressed as a dictionary
#   with keys
#     "anchor": (r, c) for upper-left corner of bag
#     "shape": index of bag on bag list

def pack(tent_size, rock_squares, bag_list):
    all_squares = set((r, c) for r in range(tent_size[0])
                                 for c in range(tent_size[1]))

    def helper(covered_squares):
        """ input: set of covered squares (covered by rocks or bags)
            output: None if no packing can be found, else a list of placed bags"""

        # all squares that are in-bounds and not covered
        open_squares = all_squares - covered_squares

        # base case: no empty squares! We return an empty (successful) packing.
        if not open_squares:
            return []

        # find the upper-left-most location
        row, col = min(open_squares)

        # here, we try placing each bag at this location
        for ix, bag in enumerate(bag_list):

            # squares covered by the bag placed at this location
            trial_squares = {(r+row, c+col) for r,c in bag}

            # if the bag contains any squares that aren't open, move on (these
            # squares could either be out-of-bounds or covered)
            if not trial_squares.issubset(open_squares):
                # don't give up and return None yet; try the next bag instead
                continue

            # if we're here, we know that placing this bag worked.  make a
            # recursive call, where all of this bag's cells are marked as
            # covered.  if it succeeds, this call will tell us how to cover all
            # the remaining cells (i.e., those not covered by this bag)
            result = helper(covered_squares | trial_squares)
            if result is not None:
                # success!  but that result doesn't contain this bag, so we
                # should include this bag in the result we return.
                return result + [{'anchor': (row, col), 'shape': ix}]

        # if we get here, we have tried all bags in this location, and none
        # worked, so we must have failed.  return None to indicate that.
        # (note that it is not necessary to include this return statement since
        # Python returns None by default, but i think it's nice to explicitly
        # signal that we're intending to return None here).
        return None

    # get things started
    return helper(rock_squares)


## A different version that works by mutation rather than by repeatedly making
## new sets/lists (maybe slightly faster and more memory efficient, especially
## for big/difficult boards

def pack(tent_size, rock_squares, bag_list):
    all_squares = {(r, c)
                   for r in range(tent_size[0])
                   for c in range(tent_size[1])}


    output = []
    rock_squares = set(rock_squares)
    def helper():
        """
        No inputs!  works by mutating output and rock_squares

        returns: True if the packing succeeded, False otherwise
        (but the result is stored in output, not returned from this helper
        function)
        """
        open_squares = all_squares - rock_squares

        if not open_squares:
            return True

        row, col = min(open_squares)
        for ix, bag in enumerate(bag_list):
            trial_squares = {(r+row, c+col) for r,c in bag}

            if not trial_squares.issubset(open_squares):
                continue

            # mutate rock_squares and output to indicate the presence of this
            # new bag
            rock_squares.update(trial_squares)
            output.append({'anchor': (row, col), 'shape': ix})

            result = helper()
            if result:
                return True

            # if we're here, the recursive call failed, so this bag didn't work!
            # we should "undo" our changes to output and rock_squares before
            # moving on to the next bag  (note also that the recursive calls
            # should have taken care of cleaning up after themselves when they
            # failed, so we only have to clean up the one bag we added).
            rock_squares.difference_update(trial_squares)
            output.pop()

        return False

    return output if helper() else None
